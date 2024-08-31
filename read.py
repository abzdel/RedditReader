import requests
import pandas as pd
import logging
import sys
import replicate
import re

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


def narrate_text(text: str, filename: str):

    deployment = replicate.deployments.get("abzdel/default-text-to-speech")
    prediction = deployment.predictions.create(
    input={"text": text}
    )
    prediction.wait()
    
    # URL of the file to download
    url = prediction.output
    print(f"url is {url}")

    # Send GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary-write mode
        with open(f'outputs/{filename}', 'wb') as f:
            # Write the content to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded file saved as {filename}")
    else:
        print("Failed to download file.")



def save_title_and_comments(title: str, df: pd.DataFrame):
    narrate_text(title, "title.mp3")

    for idx, row in df.iterrows():
        print(f"processing comment_{idx} with text {row['text']}")
        narrate_text(row['text'], f"comment_{idx}.mp3")


def clean_df(df: pd.DataFrame):
    # Use regex to remove URLs from the 'text' column
    df['text'] = df['text'].replace(r'http\S+|www.\S+', '', regex=True)
    
    df = df.sort_values(by='score', ascending=False).head(3)

    # Reset index to ensure unique and incremental indices
    df = df.reset_index(drop=True)

    return df

def main():
    #logging.basicConfig(level=logging.INFO)
    #example: url = "https://www.reddit.com/r/AskReddit/comments/1f5e6uk/whats_that_one_small_business_local_to_you_that/.json"

    url = sys.argv[1] + ".json"

    # get title
    title = get_title(requests.get(url).json())

    df = read_data(url)
    df = clean_df(df)

    save_title_and_comments(title, df)

if __name__ == "__main__":
    main()