import os
import logging
import tweepy

logger = logging.getLogger("twitter")

# client = tweepy.Client(os.environ["TWITTER_API_BEARER_TOKEN"])


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter users's original tweets (i.e., not retweets or replies) and returns them as a list of dicts.
    Each dict has three fields: 'time_posted' (relative to now), 'text' and 'url'.
    """
    client = tweepy.Client(os.environ["TWITTER_API_BEARER_TOKEN"])
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(user_id=user.id, max_results=num_tweets)

    return [
        {
            "time_posted": str(datetime.now() - tweet.created_at),
            "text": tweet.full_text,
            "url": f"https://twitter.com/{username}/status/{tweet.id}",
        }
        for tweet in tweets
    ]
