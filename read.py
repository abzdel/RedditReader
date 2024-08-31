import requests
import pandas as pd
import logging
import sys


def read_data(url: str) -> pd.DataFrame:
    logging.info(f"Reading data from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return convert_json_to_df(response.json())
    else:
        raise Exception(f"Failed to read data from {url}")
    
def convert_json_to_df(data: dict) -> pd.DataFrame:
    logging.info("Converting json to dataframe")

    comments_df = pd.DataFrame(columns=['author', 'text', 'permalink', 'score'])

    # parse comments from json, store in comments_df
    for comment_idx in range(len(data[1].get("data").get("children"))):

        current_comment = data[1].get("data").get("children")[comment_idx].get("data")
        # append each using concat
        comments_df = pd.concat([comments_df, pd.DataFrame({'author': [current_comment.get("author")],
                                                            'text': [current_comment.get("body")],
                                                            'permalink': [current_comment.get("permalink")],
                                                            'score': [current_comment.get("score")]})])
        
    return comments_df

def get_title(data: dict) -> str:
    return data[0].get("data").get("children")[0].get("data").get("title")


def main():
    logging.basicConfig(level=logging.INFO)
    # TODO change to cmd line input - add .json piece at the end
    #url = "https://www.reddit.com/r/AskReddit/comments/1f5e6uk/whats_that_one_small_business_local_to_you_that/.json"

    # take url as a flag
    url = sys.argv[1] + ".json"

    # get title
    title = get_title(requests.get(url).json())
    print(title)

    df = read_data(url)
    print(df.head())



if __name__ == "__main__":
    main()