import pandas as pd
from text_to_speech import *
import os

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_title_and_comments(title: str, df: pd.DataFrame, model: str):

    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    ensure_directory_exists(output_dir)

    df = df.sort_values(by='score', ascending=False).head(3)
    df = df.reset_index(drop=True)
    

    if model == 'eleven_labs':
        # process title
        narrate_text_eleven_labs(title, "post_title.mp3")
        
        for idx, row in df.iterrows():
            print(f"processing comment_{idx} with text {row['text']}")
            narrate_text_eleven_labs(row['text'], f"comment_{idx}.mp3")
    elif model == 'tortoise':
        # process title
        narrate_text_tortoise(title, "post_title.mp3")
        
        for idx, row in df.iterrows():
            print(f"processing comment_{idx} with text {row['text']}")
            narrate_text_tortoise(row['text'], f"comment_{idx}.mp3")

    else:
        raise Exception(f"Model {model} not supported or mistyped. Please use 'eleven_labs' or 'tortoise'.")
