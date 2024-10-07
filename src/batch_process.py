import os
import subprocess
from pull_posts import *
import sys
import io
import time
import argparse

# Ensure the default encoding is UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def process_subreddit(
    subreddit: str, num_records_to_get: int = 5, csv_output_path: str = ""
):
    df = fetch_hot_posts(
        subreddit, limit=num_records_to_get
    )  # TODO change this - may pass num_records_to_get

    idx = 0  # init idx, will be incremented for each post

    for url in df["url"]:
        print(f"Processing URL: {url}")
        try:
            # Directly call the main.py script with the URL as an argument
            result = subprocess.run(
                ["python", "src/main.py", url, str(idx), csv_output_path],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            idx += 1
            time.sleep(2)
            if result.returncode == 0:
                print(f"Successfully processed URL: {url}")
            else:
                print(f"Error processing URL: {url}. Error: {result.stderr}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--subreddit",
        type=str,
        help="The name of the subreddit to process",
        required=True,
    )

    parser.add_argument(  # TODO this has a max of 25 right now due to pull_posts limit
        "-n",
        "--num_records_to_get",
        type=int,
        help="The number of records to get from the subreddit",
        required=True,
    )

    # parse arg for csv output oath
    parser.add_argument(
        "-o",
        "--csv_output_path",
        type=str,
        help="The path to the output CSV intermediate file.",
        required=True,
    )

    args = parser.parse_args()

    subreddit_name = args.subreddit

    if not subreddit_name:
        print("No subreddit name provided. Defaulting to 'askreddit'.")
        subreddit_name = "askreddit"

    # take command line input here
    process_subreddit(
        subreddit_name,
        num_records_to_get=args.num_records_to_get,
        csv_output_path=args.csv_output_path,
    )
