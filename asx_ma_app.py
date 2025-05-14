import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price and MA20 Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price and MA20 for the Last 90 Days")
st.markdown("""
This app displays the closing price and the 20-day moving average (MA20) of Telstra (TLS.AX) for the last 90 trading days in a table format.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="90d")  # Fetch the past 90 days of data

# Clean up: Retain only 'Close' column and compute MA20
data_cleaned = data[['Close']]  # Retain only 'Close' column
data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()  # Calculate MA20

# Check if data is fetched and contains 'Close'
if data_cleaned.empty or 'Close' not in data_cleaned.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# Display the cleaned data with MA20 as a table
st.write("Telstra Closing Prices and MA20 (Last 90 Days):", data_cleaned)
