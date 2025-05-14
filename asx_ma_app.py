import streamlit as st
import yfinance as yf
import pandas as pd
import zipfile
import io

# -----------------------------
# Config
st.set_page_config(page_title="Stock Closing Price, MA20 & MA50 Table", layout="wide", page_icon="📈")
st.title("📈 Stock Closing Prices, MA20 & MA50 for the Last 180 Days")
st.markdown("""
This app fetches closing price, 20-day moving average (MA20), and 50-day moving average (MA50) for multiple stocks. You can download all selected stocks' data as separate CSV files in a single ZIP file.
""")

# -----------------------------
# List of Tickers
tickers = ["TLS.AX", "BBOZ.AX", "APX.AX", "DRO.AX"]

# Create a zip file in memory
zip_buffer = io.BytesIO()

# Create a ZIP file object
with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
    # Loop through each ticker to fetch data and add to ZIP
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
        
        # Add the CSV to the ZIP file with the stock's ticker as the file name
        zip_file.writestr(f"{ticker}_data.csv", csv_data)

# Move the pointer to the start of the ZIP buffer before sending it for download
zip_buffer.seek(0)

# -----------------------------
# Add a single download button for the ZIP file
st.download_button(
    label="Download All Stocks as ZIP",
    data=zip_buffer,
    file_name="all_stocks_data.zip",
    mime="application/zip"
)
