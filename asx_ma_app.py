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

# Check if data is empty or lacks the required columns
if data.empty or 'Close' not in data.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# -----------------------------
# Calculations
 if data.empty:
        st.warning("No data available from CoinGecko.")
        st.stop()

    data["MA20"] = data["price"].rolling(window=20).mean()
    data["MA50"] = data["price"].rolling(window=50).mean()
    data["Spread %"] = (data["MA20"] - data["MA50"]) / data["price"] * 100

    data_filtered = data.dropna(subset=["MA50"])
    if data_filtered.empty:
        st.warning("Not enough data available to calculate MA50.")
        st.stop()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(data_filtered.index, data_filtered["price"], label="Price", color="white")
    ax1.plot(data_filtered.index, data_filtered["MA20"], label="MA20", color="yellow")
    ax1.plot(data_filtered.index, data_filtered["MA50"], label="MA50", color="blue")
    ax1.set_ylabel("Price (USD)")
    ax1.legend(loc="upper left")
    ax1.set_title(f"{selected_coin_name} – Daily Chart (Last 180 Days, Starting After MA50)", color='white')

    ax2 = ax1.twinx()
    ax2.plot(data_filtered.index, data_filtered["Spread %"], label="Spread %", color="green", linestyle="dashed")
    ax2.set_ylabel("Spread %")
    ax2.legend(loc="upper right")

    st.pyplot(fig)
else:
    st.write("Select a cryptocurrency and click 'Fetch Data' to display the chart.")
