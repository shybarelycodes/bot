# File: crypto_bot/main.py
import streamlit as st
from data_fetcher import CoinGeckoAPI
import matplotlib.pyplot as plt
import time

# Initialize API
api = CoinGeckoAPI()

# Streamlit App Setup
st.set_page_config(page_title="Crypto Breakout Bot", layout="wide")
st.title("🚀 Crypto Breakout Bot")

# Step 1: Fetch Coin List
coin_list = api.get_coin_list()
selected_coins = st.multiselect("Select Cryptocurrencies to Analyze", list(coin_list.keys()), default=["bitcoin", "ethereum"])
days = st.slider("Select Historical Range (Days)", min_value=1, max_value=365, value=30)

# Step 2: Fetch and Display Data
coin_data = {}
for coin_id in selected_coins:
    try:
        data = api.get_historical_data(coin_id, "usd", days)
        coin_data[coin_id] = data
        st.subheader(f"{coin_id.capitalize()} Price Chart")
        plt.figure(figsize=(10, 4))
        plt.plot(data["timestamp"], data["price"], label=f"{coin_id} Price")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.title(f"{coin_id.capitalize()} Price Over Time")
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Failed to fetch data for {coin_id}: {e}")

# Step 3: Breakout Detection
def detect_breakouts(df, threshold=5):
    df["pct_change"] = df["price"].pct_change() * 100
    return df[df["pct_change"] > threshold]

# Display Breakout Signals
for coin_id, df in coin_data.items():
    breakouts = detect_breakouts(df)
    if not breakouts.empty:
        st.subheader(f"📈 Breakout Signals Detected for {coin_id.capitalize()}")
        st.dataframe(breakouts[["timestamp", "price", "pct_change"]])
    else:
        st.info(f"No breakout signals detected for {coin_id.capitalize()}.")

# Continuous Execution
st.sidebar.title("Continuous Operation")
run_bot = st.sidebar.checkbox("Run Bot Continuously")

if run_bot:
    st.sidebar.info("Bot is running. Do not close the browser.")
    while True:
        time.sleep(60)  # Run every 60 seconds
        st.experimental_rerun()
