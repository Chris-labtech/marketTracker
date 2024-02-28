# binance.py

import requests
from src.config import BINANCE_API_KEY

def fetch_binance_data(symbol, interval, limit):
    binance_api_url = "https://api.binance.com/api/v3/klines"

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }

    response = requests.get(binance_api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
