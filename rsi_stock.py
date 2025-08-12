import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------
# RSI Calculation Function
# -----------------------------
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="NSE RSI Dashboard", layout="wide")
st.title("📈 NSE Stock RSI Dashboard with Revenue Calculation")

# User inputs
symbol = st.text_input("Enter NSE Stock Symbol (Example: RELIANCE.NS)", "RELIANCE.NS")
start_date = st.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if st.button("Get Data"):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        
        if data.empty:
            st.error("No data found for this stock and date range.")
        else:
            data['RSI'] = calculate_rsi(data)

            # Revenue calculation: simple strategy
            # Buy when RSI < 30, Sell when RSI > 70
            data['Signal'] = 0
            data.loc[data['RSI'] < 30, 'Signal'] = 1  # Buy
            data.loc[data['RSI'] > 70, 'Signal'] = -1 # Sell

            data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
            data['Daily Return'] = data['Close'].pct_change()
            data['Strategy Return'] = data['Daily Return'] * data['Position']

            total_revenue = (data['Strategy Return'] + 1).prod() - 1

            # Plot stock price + RSI
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Close Price"))
            fig.update_layout(title=f"{symbol} Price Chart", xaxis_title="Date", yaxis_title="Price")

            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name="RSI"))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(title="RSI Chart", xaxis_title="Date", yaxis_title="RSI")

            st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(fig_rsi, use_container_width=True)

            st.subheader("📊 Revenue Calculation")
            st.write(f"Total Revenue (Strategy Return): **{total_revenue*100:.2f}%**")

            st.subheader("📄 Data Table")
            st.dataframe(data)

    except Exception as e:
        st.error(f"Error: {e}")
