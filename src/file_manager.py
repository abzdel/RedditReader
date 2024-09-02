import pandas as pd
from text_to_speech import narrate_text
import os

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_title_and_comments(title: str, df: pd.DataFrame):

    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    ensure_directory_exists(output_dir)

    df = df.sort_values(by='score', ascending=False).head(3)
    df = df.reset_index(drop=True)
    
    # process title
    narrate_text(title, "post_title.mp3")
    
    for idx, row in df.iterrows():
        print(f"processing comment_{idx} with text {row['text']}")
        narrate_text(row['text'], f"comment_{idx}.mp3")

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df['text'] = df['text'].replace(r'http\S+|www.\S+', '', regex=True)
    return df
#r8_R9Km07145al6rO6WahRmJK35Pajpszi19L1bM