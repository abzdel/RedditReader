import praw
import os
import pandas as pd

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent=os.environ.get("user_agent"),
    username=os.environ.get("reddit_user"),
    password=os.environ.get("reddit_password"),
)


def fetch_posts(subreddit: str, limit: int = 25, after: str = None) -> pd.DataFrame:
    # Fetch posts from the specified subreddit
    subreddit_instance = reddit.subreddit(subreddit)
    posts = subreddit_instance.hot(
        limit=limit, params={"after": f"t3_{after}"} if after else None
    )

    # Initialize a DataFrame
    posts_df = pd.DataFrame(columns=["title", "url", "post_id"])

    # Extract relevant information and populate the DataFrame
    for post in posts:
        posts_df = pd.concat(
            [
                posts_df,
                pd.DataFrame(
                    {
                        "title": [post.title],
                        "url": [post.url],
                        "post_id": [post.id],
                    }
                ),
            ]
        )

    posts_df = posts_df.reset_index(drop=True)
    return posts_df


# Example usage:
if __name__ == "__main__":
    subreddit_name = "AskReddit"  # Replace with your target subreddit
    top_posts_df = fetch_posts(subreddit_name)
    print(top_posts_df)
