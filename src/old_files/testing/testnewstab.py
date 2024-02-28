import requests
import tkinter as tk
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from config import NEWS_API_KEY

# Initialize NLTK and VADER
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def fetch_news_data():
    base_url = 'https://newsapi.org/v2/everything'
    
    # Calculate the date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)

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

def analyze_sentiment(text):
    # Perform sentiment analysis using VADER
    scores = sid.polarity_scores(text)
    
    # Classify the sentiment
    if scores['compound'] >= 0.05:
        return 'positive'
    elif scores['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def display_news_graph(root, news_data):
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

    # Convert the matplotlib figure to tkinter canvas
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def display_news_articles(news_tab, news_data):
    # Extract news articles
    articles = news_data.get('articles', [])

    # Sort articles based on publication date in ascending order
    sorted_articles = sorted(articles, key=lambda x: x.get('publishedAt', ''))

    # Create a treeview widget for displaying news articles
    tree = ttk.Treeview(news_tab)
    tree['columns'] = ('headline', 'url', 'date_written', 'sentiment')
    tree.heading('#0', text='Item')
    tree.column('#0', width=50, anchor='center')  # Center the content of the 'Item' column
    tree.heading('headline', text='Headline')
    tree.column('headline', width=300)
    tree.heading('url', text='URL')
    tree.column('url', width=200)
    tree.heading('date_written', text='Date Written')
    tree.column('date_written', width=150, anchor='center')  # Center the content of the 'Date Written' column
    tree.heading('sentiment', text='Sentiment')
    tree.column('sentiment', width=100, anchor='center')  # Center the content of the 'Sentiment' column

    # Insert sorted news articles into the treeview
    for i, article in enumerate(sorted_articles, 1):
        headline = article.get('title', '')
        url = article.get('url', '')
        date_written = article.get('publishedAt', '')[:10]
        sentiment = analyze_sentiment(headline)  # Analyze sentiment of the headline
        tree.insert('', 'end', text=str(i), values=(headline, url, date_written, sentiment))

    tree.pack(fill='both', expand=True)


def create_config_tab(notebook):
    # Create the frame for the config tab
    config_frame = ttk.Frame(notebook)
    notebook.add(config_frame, text="Config")

    # Add widgets to the config tab frame
    label = ttk.Label(config_frame, text="Config Tab")
    label.pack(padx=10, pady=10)

def main():
    # Fetch news data
    news_data = fetch_news_data()

    if news_data:
        # Create the tkinter window
        root = tk.Tk()
        root.title('Bitcoin News Tracker')

        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # Create tabs
        create_config_tab(notebook)

        # Display the graph in the BTC News Tracker tab
        news_tab = ttk.Frame(notebook)
        notebook.add(news_tab, text="BTC News Tracker")
        display_news_graph(news_tab, news_data)

        # Display news articles in the News Articles tab
        news_articles_tab = ttk.Frame(notebook)
        notebook.add(news_articles_tab, text="News Articles")
        display_news_articles(news_articles_tab, news_data)

        # Run the tkinter event loop
        root.mainloop()

if __name__ == "__main__":
    main()
