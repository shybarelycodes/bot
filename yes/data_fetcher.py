# File: crypto_bot/data_fetcher.py
import requests
import pandas as pd

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def get_coin_list(self):
        url = f"{self.BASE_URL}/coins/list"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.json()}")
        return {coin['id']: coin['symbol'] for coin in response.json()}

    def get_historical_data(self, coin_id: str, vs_currency: str, days: int = 30):
        url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.json()}")
        data = response.json()
        prices = data["prices"]
        volumes = data["total_volumes"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["volume"] = [vol[1] for vol in volumes]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
