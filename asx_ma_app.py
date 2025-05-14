import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="ASX Stock MA Viewer", layout="wide", page_icon="📈")
st.title("📈 ASX Stock MA Analysis")
st.markdown("""
This app shows the last 180 trading days of a selected ASX stock with:
- Closing Price
- MA20 & MA50
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
data = yf.download(ticker, period="9mo")  # Ensure enough data for 180 days

# -----------------------------
# Calculations
if 'Close' in data.columns:
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Drop rows where any required column is NaN
    data = data.dropna(subset=['MA20', 'MA50', 'Close'])

    # -----------------------------
    # Display Table
    st.subheader(f"{selected_label} - Closing Price, MA20 & MA50 (Last 180 Days)")
    st.dataframe(data[['Close', 'MA20', 'MA50']].tail(180))
else:
    st.warning("No 'Close' price data available for the selected stock.")
