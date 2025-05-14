import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price, MA20, MA50 & Spread for the Last 90 Days")
st.markdown("""
This app displays the closing price, the 20-day moving average (MA20), the 50-day moving average (MA50), and the spread between MA20 and MA50 as a percentage of the closing price for Telstra (TLS.AX) over the last 90 trading days.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="90d")  # Fetch the past 90 days of data

# Clean up: Retain only 'Close' column and compute MA20, MA50, and Spread %
data_cleaned = data[['Close']]  # Retain only 'Close' column
data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()  # Calculate MA20
data_cleaned['MA50'] = data_cleaned['Close'].rolling(window=50).mean()  # Calculate MA50

# Handle NaN values in MA20, MA50, or Close before calculating Spread %
data_cleaned['Spread%'] = ((data_cleaned['MA20'] - data_cleaned['MA50']) / data_cleaned['Close']) * 100
# Calculate Spread% only when MA20, MA50, and Close have valid data
data_cleaned['Spread%'] = None  # Initialize column with None

# Remove rows with NaN values in MA20, MA50, or Spread%
for i in range(50, len(data_cleaned)):
    if pd.notna(data_cleaned['MA20'].iloc[i]) and pd.notna(data_cleaned['MA50'].iloc[i]) and pd.notna(data_cleaned['Close'].iloc[i]):
        data_cleaned['Spread%'].iloc[i] = ((data_cleaned['MA20'].iloc[i] - data_cleaned['MA50'].iloc[i]) / data_cleaned['Close'].iloc[i]) * 100

# Drop rows with NaN values in the 'Close', 'MA20', 'MA50', or 'Spread%' columns
data_cleaned = data_cleaned.dropna(subset=['Close', 'MA20', 'MA50', 'Spread%'])

# Check if data is fetched and contains 'Close'
if data_cleaned.empty or 'Close' not in data_cleaned.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# Display the cleaned data with MA20, MA50, and Spread% as a table
st.write("Telstra Closing Prices, MA20, MA50 & Spread% (Last 90 Days):", data_cleaned)
