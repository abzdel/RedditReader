import argparse
import os
import shutil
from typing import Optional
import pandas as pd
import time
from config import Config
from reddit_client import RedditClient
from content_generator import ContentGenerator
from data_manager import DataManager

class RedditReader:
    """Main application class that orchestrates the Reddit content processing."""
    
    def __init__(self, config: Optional[Config] = None):
        if config is None:
            config = Config()
        self.config = config
        self.reddit_client = RedditClient(config)
        self.content_generator = ContentGenerator(config)
        self.data_manager = DataManager("outputs", config)

    def setup_output_directory(self, csv_output_path: str, clear_outputs: bool = True) -> None:
        """Set up output directories and optionally clear existing outputs."""
        if clear_outputs and os.path.exists(csv_output_path):
            for filename in os.listdir(csv_output_path):
                file_path = os.path.join(csv_output_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

        if not os.path.exists(csv_output_path):
            os.makedirs(csv_output_path)

    def run(self,
            subreddit: str,
            num_records_to_get: int = 5,
            csv_output_path: Optional[str] = None,
            clear_outputs: bool = True) -> None:
        """
        Main driver method to run the Reddit content processing.
        
        Args:
            subreddit (str): The name of the subreddit to process
            num_records_to_get (int): Number of records to process
            csv_output_path (Optional[str]): Path to save CSV data
            clear_outputs (bool): Whether to clear existing outputs
        """
        if csv_output_path:
            self.setup_output_directory(csv_output_path, clear_outputs)

        self.process_subreddit(
            subreddit=subreddit,
            num_records_to_get=num_records_to_get,
            csv_output_path=csv_output_path
        )

    def process_subreddit(self,
                         subreddit: str,
                         num_records_to_get: int = 5,
                         csv_output_path: Optional[str] = None) -> None:
        """Process posts from a subreddit."""
        extra_posts_factor = self.config.processing.posts_buffer_factor
        df = self.reddit_client.fetch_posts(
            subreddit,
            limit=num_records_to_get * extra_posts_factor
        )

        idx = 0
        successful_posts = 0
        post_index = 0

        while successful_posts < num_records_to_get and post_index < len(df):
            url = df.iloc[post_index]["url"]
            print(f"Processing url: {url}")

            try:
                if self.process_post(url, idx, subreddit, csv_output_path):
                    print(f"Successfully processed post at idx: {idx}")
                    idx += 1
                    successful_posts += 1
                time.sleep(self.config.processing.batch_delay)
            except Exception as e:
                print(f"An error occurred: {e}")

            post_index += 1

            if post_index >= len(df) and successful_posts < num_records_to_get:
                print(f"Fetching more posts. Currently have {successful_posts}/{num_records_to_get}")
                new_df = self.reddit_client.fetch_posts(
                    subreddit,
                    limit=num_records_to_get * extra_posts_factor,
                    after=df.iloc[-1]["post_id"]
                )
                if not new_df.empty:
                    df = pd.concat([df, new_df]).reset_index(drop=True)
                else:
                    print("No more posts available")
                    break

    def process_post(self, 
                    url: str, 
                    idx: int, 
                    subreddit: str,
                    csv_output_path: Optional[str]) -> bool:
        """Process a single Reddit post."""
        submission = self.reddit_client.get_submission(url)
        if submission is None:
            return False

        comments_df, title, post_id = self.data_manager.process_submission(submission)
        
        if csv_output_path and self.data_manager.check_duplicate_post(post_id, csv_output_path):
            print(f"Post '{title}' already exists. Skipping.")
            return False

        post_dir = self.data_manager.ensure_output_directories(idx)
        self.data_manager.save_title_id(post_id, post_dir)

        self.content_generator.generate_screenshot(
            title, 
            subreddit, 
            os.path.join(post_dir, "title_screenshot.png")
        )
        
        self.content_generator.generate_audio(
            text=title,
            filename="post_title.mp3",
            output_dir=post_dir
        )

        for i, (_, row) in enumerate(comments_df.head(self.config.processing.num_comments).iterrows()):
            self.content_generator.generate_audio(
                text=row["text"],
                filename=f"comment_{i}.mp3",
                output_dir=post_dir
            )

        if csv_output_path:
            self.data_manager.save_post_metadata(
                post_id=post_id,
                title=title,
                num_comments=self.config.processing.num_comments,
                voice=self.config.tts.voice_id,
                tts_method="eleven_labs",
                subreddit=subreddit,
                csv_output_path=csv_output_path
            )

        return True


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process Reddit posts with media generation")
    parser.add_argument(
        "-s",
        "--subreddit",
        type=str,
        help="The name of the subreddit to process",
        default="AskReddit"
    )
    parser.add_argument(
        "-n",
        "--num_records_to_get",
        type=int,
        help="The number of records to get from the subreddit",
        required=True
    )
    parser.add_argument(
        "-o",
        "--csv_output_path",
        type=str,
        help="The path to the output CSV intermediate file",
        required=True
    )
    parser.add_argument(
        "--include-nsfw",
        action="store_true",
        help="Include NSFW posts in processing"
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear existing outputs before processing"
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    config = Config(include_nsfw=args.include_nsfw)
    
    reddit_reader = RedditReader(config)
    reddit_reader.run(
        subreddit=args.subreddit,
        num_records_to_get=args.num_records_to_get,
        csv_output_path=args.csv_output_path,
        clear_outputs=not args.no_clear
    )


if __name__ == "__main__":
    # python src/main.py -p ../redditreader/outputs -bg ../backgroundvideoscraper/downloads -fo final_videos_test/ -co ../redditreader/csv_outputs
    main()