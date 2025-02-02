import praw
import pandas as pd
from typing import Optional
from config import Config


class RedditClient:
    """Handles all Reddit API interactions."""
    _instance: Optional['RedditClient'] = None

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[Config] = None):
        """Initializes the Reddit client instance if it hasn't been initialized yet."""
        if not hasattr(self, 'reddit'):
            if config is None:
                config = Config()
            
            self.reddit = praw.Reddit(
                client_id=config.reddit.client_id,
                client_secret=config.reddit.client_secret,
                user_agent=config.reddit.user_agent,
                username=config.reddit.username,
                password=config.reddit.password,
            )
            self.comment_limit = config.reddit.comment_limit
            self.include_nsfw = config.reddit.include_nsfw

    def fetch_posts(self, subreddit: str, limit: int = 25, after: str = None) -> pd.DataFrame:
        """Fetches posts from a subreddit."""
        subreddit_instance = self.reddit.subreddit(subreddit)
        posts = subreddit_instance.hot(
            limit=limit,
            params={"after": f"t3_{after}"} if after else None
        )

        posts_data = []
        for post in posts:
            posts_data.append({
                "title": post.title,
                "url": post.url,
                "post_id": post.id,
            })

        return pd.DataFrame(posts_data)

    def get_submission(self, url: str) -> Optional[praw.models.Submission]:
        """Gets a specific submission and its comments."""
        try:
            submission = self.reddit.submission(url=url)
            
            # Skip NSFW posts if include_nsfw is False
            if submission.over_18 and not self.include_nsfw:
                print(f"Skipping NSFW post: {submission.title}")
                return None
                
            if submission is None:
                print("Submission not found.")
                return None

            print(f"Submission found: {submission.title}")
            submission.comments.replace_more(limit=self.comment_limit)
            return submission
            
        except Exception as e:
            print(f"Error fetching submission: {e}")
            return None