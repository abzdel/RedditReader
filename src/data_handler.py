import requests
import pandas as pd

def read_data(url: str) -> dict:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to read data from {url}: {response.status_code}")

def convert_json_to_df(data: dict) -> pd.DataFrame:
    comments_df = pd.DataFrame(columns=['author', 'text', 'permalink', 'score'])
    for comment in data[1]['data']['children']:
        comment_data = comment['data']
        comments_df = pd.concat([comments_df, pd.DataFrame({
            'author': [comment_data.get('author')],
            'text': [comment_data.get('body')],
            'permalink': [comment_data.get('permalink')],
            'score': [comment_data.get('score')]
        })])
    return comments_df

def get_title(data: dict) -> str:
    return data[0].get("data").get("children")[0].get("data").get("title")