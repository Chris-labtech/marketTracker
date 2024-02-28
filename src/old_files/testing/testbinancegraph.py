#testbinancegraph.py

from binance.client import Client
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Get historical data for Bitcoin over the last 30 days
end_time = datetime.now()
start_time = end_time - timedelta(days=30)

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, start_time.strftime("%d %b %Y %H:%M:%S"), end_time.strftime("%d %b %Y %H:%M:%S"))

# Extracting closing prices from historical data
closing_prices = [float(entry[4]) for entry in klines]

# Generating date range for x-axis
date_range = [datetime.fromtimestamp(entry[0] / 1000) for entry in klines]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(date_range, closing_prices, label='BTC Price (USDT)')
plt.title('Bitcoin Price Over Last 30 Days')
plt.xlabel('Date')
plt.ylabel('Price (USDT)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.show()
