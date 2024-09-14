import os
import subprocess
from pull_posts import *
import sys
import io
import time

# Ensure the default encoding is UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def process_subreddit(subreddit: str, num_records_to_get: int = 3):
    df = fetch_hot_posts(subreddit, limit=num_records_to_get)

    idx = 0 # init idx, will be incremented for each post

    for url in df['url']:
        print(f"Processing URL: {url}")
        try:
            # Directly call the main.py script with the URL as an argument
            result = subprocess.run(['python', 'src/main.py', url, str(idx)], stdout=sys.stdout, stderr=sys.stderr)
            idx += 1
            time.sleep(2)
            if result.returncode == 0:
                print(f"Successfully processed URL: {url}")
            else:
                print(f"Error processing URL: {url}. Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":

    subreddit_name = sys.argv[1]
    if not subreddit_name:
        subreddit_name = "askreddit" # TODO handle this differently

    # take command line input here
    process_subreddit(subreddit_name)
