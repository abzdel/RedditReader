import os
import subprocess
from praw_pull_posts import *
import sys
import io
import time
import argparse

# Ensure the default encoding is UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def process_subreddit(
    subreddit: str, num_records_to_get: int = 5, csv_output_path: str = ""
):
    df = fetch_posts(subreddit, limit=num_records_to_get)

    idx = 0  # init idx, will be incremented for each post

    # Get the full path to the src directory
    src_directory = os.path.join(os.getcwd(), "..", "RedditReader", "src")

    for url in df["url"]:
        print(f"Processing url: {url}", flush=True)
        try:
            # Construct the full path to main.py
            main_script_path = os.path.join(src_directory, "main.py")

            # Directly call the main.py script with the URL as an argument
            result = subprocess.run(
                [
                    "python",
                    main_script_path,
                    url,
                    str(idx),
                    subreddit,
                    csv_output_path,
                ],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            time.sleep(2)
            if result.returncode == 0:
                print(
                    f"Successfully processed post_id: {url} at idx: {idx}. Incrementing idx now",
                    flush=True,
                )
                idx += 1
            else:
                print(
                    f"Error processing post_id: {url}. Not incrementing idx. Error: {result.stderr}",
                    flush=True,
                )
        except Exception as e:
            print(f"An error occurred: {e}", flush=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--subreddit",
        type=str,
        help="The name of the subreddit to process",
        required=False,
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

    if not os.path.exists(args.csv_output_path):
        os.makedirs(args.csv_output_path)
        # delete any files in the directory
        for f in os.listdir(args.csv_output_path):
            os.remove(os.path.join(args.csv_output_path, f))

    subreddit_name = args.subreddit
    print(f"subreddit_name: {subreddit_name}")

    if not subreddit_name:
        print("No subreddit name provided. Defaulting to 'AskReddit'.")
        subreddit_name = "AskReddit"

    # take command line input here
    process_subreddit(
        subreddit_name,
        num_records_to_get=args.num_records_to_get,
        csv_output_path=args.csv_output_path,
    )
