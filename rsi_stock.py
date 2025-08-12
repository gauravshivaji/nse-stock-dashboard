import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

st.title("📈 NSE Stock Technical Analysis Dashboard")

# --- Stock Input ---
stock_symbol = st.text_input("Enter NSE Stock Symbol", "RELIANCE.NS")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if st.button("Fetch Data"):
    df = yf.download(stock_symbol, start=start_date, end=end_date)

    if not df.empty:
        st.subheader(f"Stock Data for {stock_symbol}")
        st.dataframe(df.tail())

        # Simple Moving Average (SMA)
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()

        # Plot SMA
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(df.index, df['Close'], label='Close Price', color='blue')
        ax.plot(df.index, df['SMA20'], label='SMA 20', color='red')
        ax.plot(df.index, df['SMA50'], label='SMA 50', color='green')
        ax.legend()
        st.pyplot(fig)

        # You can add RSI, MACD, Bollinger Bands here
    else:
        st.error("No data found. Check symbol or date range.")
