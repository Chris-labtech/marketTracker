import tkinter as tk
from tkinter import ttk
from binance.client import Client
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from config import BINANCE_API_KEY, BINANCE_API_SECRET

# Fetching API details
api_key = 'BINANCE_API_KEY'
api_secret = 'BINANCE_API_SECRET'

# Create Binance client
client = Client(api_key, api_secret)

def fetch_and_plot_data(symbol):
    # Get historical data for the selected symbol over the last 30 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)

    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_time.strftime("%d %b %Y %H:%M:%S"), end_time.strftime("%d %b %Y %H:%M:%S"))

    # Extracting closing prices from historical data
    closing_prices = [float(entry[4]) for entry in klines]

    # Generating date range for x-axis
    date_range = [datetime.fromtimestamp(entry[0] / 1000) for entry in klines]

    # Plotting the data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(date_range, closing_prices, label=f'{symbol} Price (USDT)')
    ax.set_title(f'{symbol} Price Over Last 30 Days')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USDT)')
    ax.grid(True)
    ax.legend()

    # Embedding matplotlib figure into tkinter window
    canvas = FigureCanvasTkAgg(fig, master=tab1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_symbol_select(event):
    selected_symbol = symbol_var.get()
    fetch_and_plot_data(selected_symbol)

# Create tkinter window
root = tk.Tk()
root.title("Cryptocurrency Price Analysis")

# Create notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text='Price Graph')

# Create symbol selection dropdown
symbol_var = tk.StringVar(tab1)
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"]  # Add more symbols as needed
symbol_dropdown = ttk.Combobox(tab1, textvariable=symbol_var, values=symbols)
symbol_dropdown.bind("<<ComboboxSelected>>", on_symbol_select)
symbol_dropdown.pack(pady=10)

root.mainloop()
