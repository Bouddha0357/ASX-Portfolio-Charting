import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# -----------------------------
# Config
st.set_page_config(page_title="Telstra Closing Price Chart", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) - Closing Price for the Last 90 Days")
st.markdown("""
This app displays the closing price of Telstra (TLS.AX) for the last 90 trading days.
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

# Debugging: Show the cleaned data for verification
st.write("Cleaned Data (Last 90 Days):", data_cleaned.head())  # Display cleaned data

# -----------------------------
# Plotly Chart - Closing Price
fig = go.Figure()

# Closing Price
fig.add_trace(go.Scatter(x=data_cleaned.index, y=data_cleaned["Close"], mode='lines', name="Closing Price", line=dict(color="lightblue")))

# Layout
fig.update_layout(
    template="plotly_dark",
    title="Telstra (TLS.AX) - Closing Price (Last 90 Days)",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Closing Price (AUD)"),
    legend=dict(x=0, y=1.2, orientation="h")
)

# -----------------------------
# Display Chart
st.plotly_chart(fig, use_container_width=True)
