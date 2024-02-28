# news_tracker.py
import requests
import tkinter as tk
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config import NEWS_API_KEY

def fetch_news_data():
    base_url = 'https://newsapi.org/v2/everything'
    
    # Calculate the date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Format dates as strings in the required format (YYYY-MM-DD)
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')

    # Specify parameters for the request
    params = {
        'q': 'bitcoin',
        'from': from_date,
        'to': to_date,
        'apiKey': NEWS_API_KEY,
    }

    # Make the request to the News API
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if the request was successful

        # Parse the JSON response
        news_data = response.json()
        return news_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None

def display_news_graph(news_data):
    # Extract dates and count the number of articles per day
    articles = news_data.get('articles', [])
    date_count = {}
    for article in articles:
        published_at = article['publishedAt'][:10]  # Extracting the date part
        date_count[published_at] = date_count.get(published_at, 0) + 1

    # Create a sorted list of dates and corresponding article counts
    dates_sorted = sorted(date_count.keys())
    article_counts_sorted = [date_count[date] for date in dates_sorted]

    # Plot the graph
    plt.figure(figsize=(8, 4))
    plt.plot(dates_sorted, article_counts_sorted, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.title('Number of Articles About Bitcoin in the Last 30 Days')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def main():
    # Fetch news data
    news_data = fetch_news_data()

    if news_data:
        # Display the graph
        display_news_graph(news_data)

if __name__ == "__main__":
    main()
