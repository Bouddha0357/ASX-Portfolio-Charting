import streamlit as st
import yfinance as yf
import pandas as pd

# -----------------------------
# Config
st.set_page_config(page_title="Stock Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Stock Closing Prices, MA20 & MA50 for the Last 180 Days")
st.markdown("""
This app fetches closing price, 20-day moving average (MA20), and 50-day moving average (MA50) for multiple stocks. You can download the data for each selected stock as a separate CSV file.
""")

# -----------------------------
# List of Tickers
tickers = ["TLS.AX", "BBOZ.AX", "APX.AX", "DRO.AX"]

# Loop through each ticker to fetch data and add download buttons
for ticker in tickers:
    # Fetch the past 180 days of data for each ticker
    data = yf.download(ticker, period="180d")  
    
    # Clean up: Retain only 'Close' column and compute MA20 and MA50
    data_cleaned = data[['Close']]  # Retain only 'Close' column
    data_cleaned['MA20'] = data_cleaned['Close'].rolling(window=20).mean()  # Calculate MA20
    data_cleaned['MA50'] = data_cleaned['Close'].rolling(window=50).mean()  # Calculate MA50
    
    # Add the ticker symbol as a column
    data_cleaned['Ticker'] = ticker
    
    # Convert the DataFrame to CSV format
    csv_data = data_cleaned.to_csv(index=True)  # Convert data to CSV format
    
    # Add a download button for each stock's CSV
    st.download_button(
        label=f"Download {ticker} CSV",
        data=csv_data,
        file_name=f"{ticker}_data.csv",
        mime="text/csv"
    )
