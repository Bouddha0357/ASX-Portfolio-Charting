import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price for the Last 90 Days")
st.markdown("""
This app displays the closing price of Telstra (TLS.AX) for the last 90 trading days in a table format.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="90d")  # Fetch the past 90 days of data

# Clean up: Drop any unnecessary columns (we only need 'Close')
data_cleaned = data[['Close']]  # Retain only 'Close' column

# Check if data is fetched and contains 'Close'
if data_cleaned.empty or 'Close' not in data_cleaned.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# Display the cleaned data as a table
st.write("Telstra Closing Prices (Last 90 Days):", data_cleaned)
