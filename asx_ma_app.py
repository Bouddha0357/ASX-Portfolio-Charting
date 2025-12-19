import streamlit as st
import yfinance as yf
import pandas as pd
import io

# -----------------------------
# Config
st.set_page_config(page_title="ASX Emerging Companies Stock Data Downloader", layout="wide", page_icon="📈")
st.title("📈 Portfolio Stock Data Downloader - Closing Price, MA20 & MA50 (Last 180 Days)")

# -----------------------------
# ASX Ticker List (from your screenshot)
tickers = [
    "TLS",  "APX",  "AXE",  "AL3",  "ALC",  "DRO"
]

# Add ".AX" to each ticker for Yahoo Finance
tickers = [ticker + ".AX" for ticker in tickers]

# Combined DataFrame
all_data = []

# -----------------------------
# Fetch and process data
with st.spinner("Fetching data, please wait..."):
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="180d", progress=False)
            if data.empty or 'Close' not in data.columns:
                continue
            
            # Create a new DataFrame with just the 'Close' column
            data_cleaned = pd.DataFrame()
            data_cleaned['Close'] = data['Close']
            data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()
            data_cleaned['MA50'] = data_cleaned['Close'].rolling(window=50).mean()
            data_cleaned['Ticker'] = ticker.replace(".AX", "")
            data_cleaned.reset_index(inplace=True)
            all_data.append(data_cleaned)

        except Exception as e:
            st.warning(f"Failed to fetch data for {ticker}: {e}")

# Combine all into one CSV
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    csv_buffer = io.StringIO()
    combined_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Combined CSV for All Stocks",
        data=csv_buffer.getvalue(),
        file_name="asx_portfolio_data.csv",
        mime="text/csv"
    )
else:
    st.error("No data was fetched. Please try again later or check ticker symbols.")








