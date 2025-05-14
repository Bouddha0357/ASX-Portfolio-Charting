import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Config
st.set_page_config(page_title="ASX Stock MA Viewer", layout="wide", page_icon="📈")
st.title("📈 ASX Stock MA Analysis")
st.markdown("""
This app shows the last 90 trading days of a selected ASX stock with:
- Price
- MA20 & MA50
- Spread (% of price) between MA20 and MA50
""")

# -----------------------------
# Dropdown
stock_map = {
    "Telstra (TLS)": "TLS.AX",
    "BBOZ": "BBOZ.AX",
    "Appen (APX)": "APX.AX",
    "DroneShield (DRO)": "DRO.AX"
}

selected_label = st.selectbox("Select ASX Stock:", list(stock_map.keys()))
ticker = stock_map[selected_label]

# -----------------------------
# Data Fetching
data = yf.download(ticker, period="6mo")  # To ensure enough data for MA50
data = data.tail(90 + 50)  # Ensure room for MA50 to appear

# -----------------------------
# Calculations
if 'Close' in data.columns:
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Drop rows until MA50 is available
    data = data.dropna(subset=['MA20', 'MA50', 'Close'])

    data['SpreadPct'] = ((data['MA20'] - data['MA50']) / data['Close']) * 100

    # -----------------------------
    # Plotly Chart
    fig = go.Figure()

    # Price
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Price', line=dict(color='lightblue')))

    # MA20 & MA50
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], mode='lines', name='MA20', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='MA50', line=dict(color='green')))

    # Spread % on secondary y-axis
    fig.add_trace(go.Scatter(x=data.index, y=data['SpreadPct'], mode='lines', name='Spread % (MA20 - MA50)', yaxis='y2', line=dict(color='red', dash='dot')))

    # Layout
    fig.update_layout(
        template='plotly_dark',
        title=f"{selected_label} - Price, MA20, MA50 & Spread %",
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        yaxis2=dict(title='Spread %', overlaying='y', side='right'),
        legend=dict(x=0, y=1.2, orientation='h')
    )

    # -----------------------------
    # Display Chart
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No 'Close' price data available for the selected stock.")
