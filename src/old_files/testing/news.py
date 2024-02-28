# src/data_collection/news.py
import requests
from config import API_KEYS

def get_news(api_key):
    endpoint = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': 'bitcoin',  # Search query for Bitcoin-related news
        'language': 'en',
    }

    response = requests.get(endpoint, params=params)
    news_data = response.json()

    return news_data

# Uncomment the line below if you want to run the get_news function when this file is executed
# news_data = get_news(API_KEYS['news'])
# print(news_data)
