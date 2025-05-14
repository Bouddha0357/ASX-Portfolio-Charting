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
    st.warning(f"No valid price data returned for {ticker}. It may be
