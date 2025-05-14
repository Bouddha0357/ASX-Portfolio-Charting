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

# Check if data is fetched correctly and display first few rows for debugging
st.write("Fetched data:", data.head())  # Display first few rows for debugging

# Clean up data: Keep only the "Close" column and drop other unnecessary columns
data = data[['Close']]  # Keep only the "Close" column

# Check if data is available and contains 'Close' column
if data.empty or 'Close' not in data.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# -----------------------------
# Plotly Chart - Closing Price
fig = go.Figure()

# Closing Price
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name="Closing Price", line=dict(color="lightblue")))

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
