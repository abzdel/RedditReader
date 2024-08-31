import pandas as pd
from text_to_speech import narrate_text

def save_title_and_comments(title: str, df: pd.DataFrame):
    df = df.sort_values(by='score', ascending=False).head(3)
    df = df.reset_index(drop=True)
    
    for idx, row in df.iterrows():
        print(f"processing comment_{idx} with text {row['text']}")
        narrate_text(row['text'], f"comment_{idx}.mp3")

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df['text'] = df['text'].replace(r'http\S+|www.\S+', '', regex=True)
    return df
