import tweepy
from textblob import TextBlob
from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET


# Authenticate
auth = tweepy.OAuth1UserHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Search query
query = 'Bitcoin'

# Fetch tweets
tweets = api.search_tweets(q=query, count=100)

total_likes = 0
total_retweets = 0
positive_sentiments = 0
negative_sentiments = 0
neutral_sentiments = 0

for tweet in tweets:
    # Likes and retweets
    total_likes += tweet.favorite_count
    total_retweets += tweet.retweet_count
    
    # Sentiment analysis
    analysis = TextBlob(tweet.text)
    if analysis.sentiment.polarity > 0:
        positive_sentiments += 1
    elif analysis.sentiment.polarity < 0:
        negative_sentiments += 1
    else:
        neutral_sentiments += 1

print("Total Likes:", total_likes)
print("Total Retweets:", total_retweets)
print("Positive Sentiments:", positive_sentiments)
print("Negative Sentiments:", negative_sentiments)
print("Neutral Sentiments:", neutral_sentiments)
