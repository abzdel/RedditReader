import requests
import pandas as pd
import warnings
import time

warnings.filterwarnings("ignore")


def read_data(url: str) -> dict:
    # Read data from the provided URL
    # infinite loop - retry in 5 seconds if rate limited
    while True:
        try:
            response = requests.get(url)
            return response.json()
        except:
            print("Failed to fetch data from Reddit. Retrying in 5 seconds...")
            time.sleep(5)


def convert_json_to_df(data: dict) -> pd.DataFrame:
    comments_df = pd.DataFrame(columns=["author", "text", "permalink", "score"])
    for comment in data[1]["data"]["children"]:
        comment_data = comment["data"]
        comments_df = pd.concat(
            [
                comments_df,
                pd.DataFrame(
                    {
                        "author": [comment_data.get("author")],
                        "text": [comment_data.get("body")],
                        "permalink": [comment_data.get("permalink")],
                        "score": [comment_data.get("score")],
                    }
                ),
            ]
        )
    return comments_df


def get_title(data: dict) -> str:
    title = data[0].get("data").get("children")[0].get("data").get("title")
    title_id = data[0].get("data").get("children")[0].get("data").get("id")
    return title, title_id


def get_author(data: dict) -> str:
    return data[0].get("data").get("children")[0].get("data").get("author")


def clean_df(df: pd.DataFrame, max_characters: int) -> pd.DataFrame:

    # drop rows where text is > max_characters
    df = df[df["text"].str.len() <= max_characters]

    # remove URLs from text
    # TODO consider just deleting these comments - some posts with websites may need the link for context
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
