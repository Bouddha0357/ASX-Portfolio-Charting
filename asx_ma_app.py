import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Config
st.set_page_config(page_title="Telstra MA50 Chart", layout="wide", page_icon="📈")
st.title("📈 Telstra (TLS.AX) MA50 Analysis")
st.markdown("""
This app fetches the 50-day moving average (MA50) of Telstra (TLS.AX) for the past 90 days and displays it on a chart.
""")

# -----------------------------
# Data Fetching
ticker = "TLS.AX"
data = yf.download(ticker, period="90d")  # Fetch the past 90 days of data

# Check if data is available
if data.empty or 'Close' not in data.columns:
    st.warning(f"No valid price data returned for {ticker}. It may be unavailable on Yahoo Finance.")
    st.stop()

# -----------------------------
# Calculate MA50
data["MA50"] = data["Close"].rolling(window=50).mean()

# -----------------------------
# Plotly Chart
fig = go.Figure()

# Price
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name="Price", line=dict(color="lightblue")))

# MA50
fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode='lines', name="MA50", line=dict(color="orange")))

# Layout
fig.update_layout(
    template="plotly_dark",
    title="Telstra (TLS.AX) - 50-day Moving Average (MA50)",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Price"),
    legend=dict(x=0, y=1.2, orientation="h")
)

# -----------------------------
# Display Chart
st.plotly_chart(fig, use_container_width=True)
