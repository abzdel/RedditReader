import sys
from data_handler import read_data, convert_json_to_df, get_title, clean_df
from file_manager import save_title_and_comments

def main():
    url = sys.argv[1] + ".json"

    # Get data and process
    data = read_data(url)
    title = get_title(data)
    df = convert_json_to_df(data)
    df = clean_df(df, max_characters=200) # long posts break the TTS model

    save_title_and_comments(title, df)

if __name__ == "__main__":
    main()
