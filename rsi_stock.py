import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import ta

# --------------------
# Streamlit Page Config
# --------------------
st.set_page_config(page_title="NSE Stock Technical Analysis Dashboard", layout="wide")

st.title("📊 NSE Stock Technical Analysis Dashboard")
st.markdown("Analyze SMA, RSI, MACD, and Bollinger Bands for NSE stocks in real time.")

# --------------------
# Sidebar Inputs
# --------------------
st.sidebar.header("Stock & Settings")
nse_symbol = st.sidebar.text_input(
    "Enter NSE stock symbol (with .NS)", value="RELIANCE.NS"
)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# --------------------
# Fetch Data
# --------------------
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    df.dropna(inplace=True)
    return df

if st.sidebar.button("Load Data"):
    df = load_data(nse_symbol, start_date, end_date)

    if df.empty:
        st.error("No data found. Check symbol or date range.")
    else:
        st.subheader(f"Price Data: {nse_symbol}")
        st.write(df.tail())

        # --------------------
        # Technical Indicators
        # --------------------
        df["SMA20"] = ta.trend.sma_indicator(df["Close"], window=20)
        df["SMA50"] = ta.trend.sma_indicator(df["Close"], window=50)
        df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
        macd = ta.trend.MACD(df["Close"])
        df["MACD"] = macd.macd()
        df["MACD_Signal"] = macd.macd_signal()
        bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
        df["BB_High"] = bb.bollinger_hband()
        df["BB_Low"] = bb.bollinger_lband()

        # --------------------
        # Plots
        # --------------------
        st.subheader("📈 Price Chart with SMA & Bollinger Bands")
        fig, ax = plt.subplots(figsize=(12,6))
        ax.plot(df.index, df["Close"], label="Close Price")
        ax.plot(df.index, df["SMA20"], label="SMA 20", linestyle="--")
        ax.plot(df.index, df["SMA50"], label="SMA 50", linestyle="--", color="magenta")
        ax.plot(df.index, df["BB_High"], label="BB High", linestyle=":", color="red")
        ax.plot(df.index, df["BB_Low"], label="BB Low", linestyle=":", color="green")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 RSI (Relative Strength Index)")
        fig, ax = plt.subplots(figsize=(12,3))
        ax.plot(df.index, df["RSI"], label="RSI", color="orange")
        ax.axhline(70, color="red", linestyle="--")
        ax.axhline(30, color="green", linestyle="--")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 MACD")
        fig, ax = plt.subplots(figsize=(12,3))
        ax.plot(df.index, df["MACD"], label="MACD", color="blue")
        ax.plot(df.index, df["MACD_Signal"], label="Signal", color="red")
        ax.legend()
        st.pyplot(fig)

        # --------------------
        # Signal Logic Example
        # --------------------
        latest = df.iloc[-1]
        signal = None
        if latest["RSI"] < 30 and latest["Close"] > latest["BB_Low"]:
            signal = "Possible Buy Signal (Oversold)"
        elif latest["RSI"] > 70 and latest["Close"] < latest["BB_High"]:
            signal = "Possible Sell Signal (Overbought)"

        if signal:
            st.success(signal)
        else:
            st.info("No strong signal detected currently.")
else:
    st.info("Enter stock details and click 'Load Data'.")
