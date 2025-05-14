import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price, MA20 & MA50 for the Last 180 Days")
st.markdown("""
This app displays the closing price, the 20-day moving average (MA20), the 50-day moving average (MA50), and the difference (MA20 - MA50) divided by the closing price of Telstra (TLS.AX) for the last 180 trading days in a table format.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="180d")  # Fetch the past 180 days of data

# Clean up: Retain only 'Close' column and compute MA20 and MA50
data_cleaned = data[['Close']]  # Retain only 'Close' column
data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()  # Calculate MA20
data_cleaned['MA50'] = data_cleaned['Close'].rolling(window=50).mean()  # Calculate MA50

# Calculate (MA20 - MA50) / Closing Price, and set the first 50 rows to NaN (since MA50 starts at day 50)
data_cleaned['MA20 - MA50 / Close'] = (data_cleaned['MA20'] - data_cleaned['MA50']) / data_cleaned['Close']
data_cleaned['MA20 - MA50 / Close'][:50] = pd.NA  # Set the first 50 rows to NaN

# Check if data is fetched and contains 'Close'
if data_cleaned.empty or 'Close' not in data_cleaned.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# Display the cleaned data with MA20, MA50, and MA20 - MA50 / Closing Price as a table
st.write("Telstra Closing Prices, MA20, MA50, and (MA20 - MA50) / Closing Price (Last 180 Days):", data_cleaned)
