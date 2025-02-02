import pandas as pd
import os
import csv
from typing import Optional, Tuple
from datetime import datetime
import praw
from .config import Config

class DataManager:
    """Handles both data processing and file operations."""
    
    def __init__(self, base_output_dir: str, config: Optional[Config] = None):
        self.base_output_dir = base_output_dir
        if config is None:
            config = Config()
        self.config = config

    def process_submission(self, submission: praw.models.Submission) -> Tuple[pd.DataFrame, str, str]:
        """Processes a submission and returns cleaned comments DataFrame and metadata."""
        comments_df = self._create_comments_df(submission)
        comments_df = self._clean_comments(comments_df, self.config.processing.max_characters)
        
        title = submission.title
        post_id = submission.id
        
        return comments_df, title, post_id

    def ensure_output_directories(self, idx: int) -> str:
        """Creates and ensures output directories exist."""
        post_dir = os.path.join(self.base_output_dir, f"post_{idx}")
        os.makedirs(post_dir, exist_ok=True)
        return post_dir

    def save_post_metadata(self, 
                         post_id: str,
                         title: str,
                         num_comments: int,
                         voice: str,
                         tts_method: str,
                         subreddit: str,
                         csv_output_path: str) -> bool:
        """
        Saves post metadata to CSV.
        Returns True if successful, False otherwise.
        """
        try:
            data_dict = {
                "post_id": post_id,
                "title": title,
                "generation_date": datetime.now().isoformat(),
                "num_comments": num_comments,
                "uploaded": False,
                "uploaded_date": None,
                "voice_model": voice,
                "tts_method": tts_method,
                "subreddit": subreddit,
                "bg_video": None
            }

            csv_path = os.path.join(csv_output_path, "data.csv")
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)

            file_exists = os.path.exists(csv_path)
            with open(csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data_dict.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data_dict)

            print(f"Saved metadata for '{title}' to {csv_path}")
            return True
            
        except Exception as e:
            print(f"Error saving metadata: {e}")
            return False

    def check_duplicate_post(self, post_id: str, csv_output_path: str) -> bool:
        """Checks if a post already exists in the CSV."""
        csv_path = os.path.join(csv_output_path, "data.csv")
        
        if not os.path.exists(csv_path):
            return False
            
        try:
            df = pd.read_csv(csv_path, encoding="ISO-8859-1")
            return post_id in df["post_id"].values
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False

    def save_title_id(self, title_id: str, output_path: str) -> bool:
        """
        Saves the title ID to a file.
        Returns True if successful, False otherwise.
        """
        try:
            with open(os.path.join(output_path, "title_id.txt"), "w") as f:
                f.write(title_id)
            return True
        except Exception as e:
            print(f"Error saving title ID: {e}")
            return False

    def _create_comments_df(self, submission: praw.models.Submission) -> pd.DataFrame:
        """Creates a DataFrame from submission comments.
        
        Args:
            submission (praw.models.Submission): Submission object.
        
        Returns:
            pd.DataFrame: DataFrame of comments.
        """
        comments = []
        for comment in submission.comments.list():
            comments.append({
                # we can always add more columns from comments here
                "author": comment.author.name if comment.author else None,
                "text": comment.body,
                "permalink": comment.permalink,
                "score": comment.score
            })
        return pd.DataFrame(comments)

    def _clean_comments(self, df: pd.DataFrame, max_characters: int) -> pd.DataFrame:
        """
        Cleans and filters comments DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame of comments.
            max_characters (int): Maximum number of characters in comment text.
        
        Returns:
            pd.DataFrame: Cleaned DataFrame of comments.

        TODO: Add more cleaning methods
        """
        # filter by length
        df = df[df["text"].str.len() <= max_characters].copy()
        
        # clean text
        df.loc[:, "text"] = (df["text"]
            .str.replace(r"http\S+|www.\S+", "", regex=True)
            .str.replace("-", ",")
            .str.replace("*", ""))
        
        # remove deleted/removed comments and clean
        df = df[
            ~df["text"].str.contains(r"\[deleted\]") & 
            ~df["text"].str.contains(r"\[removed\]")
        ].dropna(subset=["text"])
        
        return df.sort_values(by="score", ascending=False)