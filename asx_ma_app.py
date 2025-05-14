import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price, MA20 & MA50 for the Last 180 Days")
st.markdown("""
This app displays the closing price, the 20-day moving average (MA20), the 50-day moving average (MA50), and the percentage difference ((MA20 - MA50) / Closing Price) of Telstra (TLS.AX) for the last 180 trading days in a table format.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="180d")  # Fetch the past 180 days of data

# Clean up: Retain only 'Close' column and compute MA20 and MA50
data_cleaned = data[['Close']]  # Retain only 'Close' column
data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()  # Calculate MA20
data_cleaned['MA50'] = data_cleaned['Close'].rolling(window=50).mean()  # Calculate MA50

# Calculate ((MA20 - MA50) / Closing Price) * 100 to get the percentage, and set the first 50 rows to NaN
data_cleaned['Spread %'] = ((data_cleaned['MA20'] - data_cleaned['MA50']) / data_cleaned['Close']) * 100
data_cleaned['Spread %'][:50] = pd.NA  # Set the first 50 rows to NaN

# Check if data is fetched and contains 'Close'
if data_cleaned.empty or 'Close' not in data_cleaned.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# Format the 'Spread %' column as a percentage with 2 decimal places
data_cleaned['Spread %'] = data_cleaned['Spread %'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "")

# Display the cleaned data as a dataframe
st.dataframe(data_cleaned)
