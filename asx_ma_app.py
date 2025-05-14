import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price, MA20 & MA50 for the Last 180 Days")
st.markdown("""
This app displays the closing price, the 20-day moving average (MA20), and the 50-day moving average (MA50) of Telstra (TLS.AX) for the last 180 trading days in a table format.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="9mo")  # Ensure enough data for 180 days

# -----------------------------
# Calculations
required_cols = ['Close']
if all(col in data.columns for col in required_cols):
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Determine available columns and drop rows only where all exist
    available_cols = ['Close']
    if 'MA20' in data.columns:
        available_cols.append('MA20')
    if 'MA50' in data.columns:
        available_cols.append('MA50')

    data = data.dropna(subset=available_cols)

    if not data.empty and all(col in data.columns for col in ['Close', 'MA20', 'MA50']):
        # -----------------------------
        # Display Table
        st.subheader("Telstra - Closing Price, MA20 & MA50 (Last 180 Days)")
        st.dataframe(data[['Close', 'MA20', 'MA50']].tail(180))
    else:
        st.warning("Not enough data available to compute MA20 and MA50.")
else:
    st.warning("No 'Close' price data available for the selected stock.")
