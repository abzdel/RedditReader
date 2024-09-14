import os
import subprocess
from pull_posts import *
import sys
import io
import time

# Ensure the default encoding is UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def process_subreddit(subreddit: str):
    df = fetch_hot_posts(subreddit, limit=5)

    for url in df['url']:
        print(f"Processing URL: {url}")
        try:
            # Directly call the main.py script with the URL as an argument
            result = subprocess.run(['python', 'src/main.py', url], capture_output=True, text=True)
            time.sleep(2)
            if result.returncode == 0:
                print(f"Successfully processed URL: {url}")
            else:
                print(f"Error processing URL: {url}. Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")
        break

if __name__ == "__main__":
    subreddit_name = "askreddit"  # Replace with your target subreddit
    # take command line input here
    process_subreddit(subreddit_name)
