import praw
import pandas as pd
import warnings
import os

warnings.filterwarnings("ignore")

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent=os.environ.get("user_agent"),
    username=os.environ.get("reddit_user"),
    password=os.environ.get("reddit_password"),
)


def read_data(url: str) -> dict:
    while True:
        submission = reddit.submission(url=url)

        if submission is None:
            print("Submission not found. Retrying in 5 seconds...")
            continue

        break
    print(f"Submission found: {submission.title}")

    # Fetch post comments
    submission.comments.replace_more(limit=5)  # Load all comments

    # if submission is over18, return None
    # if submission.over_18:
    #     print("Submission is over 18. Skipping...")
    #     return None
    return submission


def convert_json_to_df(submission) -> pd.DataFrame:
    comments_df = pd.DataFrame(columns=["author", "text", "permalink", "score"])
    for comment in submission.comments.list():
        comments_df = pd.concat(
            [
                comments_df,
                pd.DataFrame(
                    {
                        "author": [comment.author.name if comment.author else None],
                        "text": [comment.body],
                        "permalink": [comment.permalink],
                        "score": [comment.score],
                    }
                ),
            ]
        )
    return comments_df


def get_title(submission) -> str:
    title = submission.title
    title_id = submission.id
    return title, title_id


def get_author(submission) -> str:
    return submission.author.name if submission.author else None


def clean_df(df: pd.DataFrame, max_characters: int) -> pd.DataFrame:
    # drop rows where text is > max_characters
    df = df[df["text"].str.len() <= max_characters]

    # remove URLs from text
    df.loc[:, "text"] = df["text"].replace(r"http\S+|www.\S+", "", regex=True)

    # Drop rows where 'text' is None
    df = df.dropna(subset=["text"])

    # if text contains '[deleted]', strip it
    df = df[~df["text"].str.contains(r"\[deleted\]")]

    # if text contains ['removed'], strip it
    df = df[~df["text"].str.contains(r"\[removed\]")]

    # replace hyphens with commas
    df["text"] = df["text"].str.replace("-", ",")
    df["text"] = df["text"].str.replace("*", "")

    return df
