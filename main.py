import os
from dotenv import load_dotenv
import os
import json
import shutil
import logging
import os
from src.TwitterPoster import TwitterPoster

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='tweet_posting.log'
)

def process_json_tweets(
    input_directory, 
    processed_directory, 
    error_directory,
    consumer_key, 
    consumer_secret, 
    access_token, 
    access_token_secret,
    BEARER_TOKEN
):
    """
    Process JSON tweet files, post tweets, and manage file movement
    
    Args:
        input_directory (str): Directory containing tweet JSON files
        processed_directory (str): Directory to move successfully posted tweets
        error_directory (str): Directory to move tweets that failed to post
        consumer_key (str): Twitter API consumer key
        consumer_secret (str): Twitter API consumer secret
        access_token (str): Twitter API access token
        access_token_secret (str): Twitter API access token secret
    """
    # Ensure directories exist
    print("Start processing ...")
    for directory in [input_directory, processed_directory, error_directory]:
        os.makedirs(directory, exist_ok=True)

    # Initialize Twitter poster
    print("Initialize Twitter Poster ...")
    twitter_poster = TwitterPoster(
        consumer_key, 
        consumer_secret, 
        access_token, 
        access_token_secret,
        BEARER_TOKEN
    )

    # Process JSON files
    print("Process JSON files ...")
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            print(f"Processing {file_path} ...")
            
            # Read JSON file
            print(f"Reading JSON file {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as file:
                tweet_data = json.load(file)
            
            # Extract tweet details
            print(f"Extracting tweet details ...")
            content = tweet_data.get('content', '')
            hashtags = tweet_data.get('hashtags', '')
            
            # Post tweet
            print(f"Posting tweet ...")
            if twitter_poster.post_tweet(content, hashtags):
                # Move to processed directory
                print(f"Moving {filename} to processed directory {processed_directory} ...")
                processed_file_path = os.path.join(
                    processed_directory, 
                    f"processed_{filename}"
                )
                shutil.move(file_path, processed_file_path)
                logging.info(f"Moved {filename} to processed directory")
            else:
                # Move to error directory
                print(f"Moving {filename} to error directory {error_directory} ...")
                error_file_path = os.path.join(
                    error_directory, 
                    f"error_{filename}"
                )
                shutil.move(file_path, error_file_path)
                logging.warning(f"Moved {filename} to error directory")

if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()
    
    # Replace with your actual Twitter API credentials
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    
    # Directories
    INPUT_DIR = os.getenv('INPUT_DIR')
    PROCESSED_DIR = os.getenv('PROCESSED_DIR')
    ERROR_DIR = os.getenv('ERROR_DIR')

    # Process tweets
    process_json_tweets(
        INPUT_DIR, 
        PROCESSED_DIR, 
        ERROR_DIR,
        CONSUMER_KEY, 
        CONSUMER_SECRET, 
        ACCESS_TOKEN, 
        ACCESS_TOKEN_SECRET,
        BEARER_TOKEN
    )