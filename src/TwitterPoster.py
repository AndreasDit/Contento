import tweepy
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='tweet_posting.log'
)

class TwitterPoster:
    def __init__(self, 
                consumer_key, 
                consumer_secret, 
                access_token, 
                access_token_secret,
                BEARER_TOKEN):
        """
        Initialize Twitter API connection
        
        Args:
            consumer_key (str): Twitter API consumer key
            consumer_secret (str): Twitter API consumer secret
            access_token (str): Twitter API access token
            access_token_secret (str): Twitter API access token secret
        """
        try:
            # Twitter API authentication
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            
            # Create API object
            self.api = tweepy.API(auth)
            
            # Create API v2 object
            self.api_v2 = tweepy.Client(
                bearer_token=BEARER_TOKEN,
                access_token=access_token,
                access_token_secret=access_token_secret,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
            )
        except Exception as e:
            logging.error(f"Twitter API Authentication Failed: {e}")
            raise

    def post_tweet(self, content, hashtags=''):
        """
        Post a tweet with optional hashtags
        
        Args:
            content (str): Tweet text
            hashtags (str, optional): Hashtags to append to tweet
        
        Returns:
            bool: True if tweet posted successfully, False otherwise
        """
        # Combine content and hashtags
        full_tweet = f"{content} {hashtags}".strip()
        
        # Check tweet length (280 characters max)
        if len(full_tweet) > 280:
            logging.warning(f"Tweet too long. Truncating to 280 characters.")
            full_tweet = full_tweet[:280]
        
        # Post tweet
        self.api_v2.create_tweet(text=full_tweet)
        logging.info(f"Successfully posted tweet: {full_tweet}")