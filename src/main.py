import sys
from data_handler import read_data, convert_json_to_df, get_title, clean_df
from file_manager import save_title_and_comments

def main():
    # if url ends with a slash, remove it
    if sys.argv[1][-1] == "/":
        url = sys.argv[1][:-1] + ".json"
    else:
        url = sys.argv[1] + ".json"

    try:
        idx = int(sys.argv[2])
    except:
        idx = 0

    # if no idx is provided, set it to 0
    if not idx:
        idx = 0

    # Get data and process
    data = read_data(url)
    title = get_title(data)
    df = convert_json_to_df(data)
    df = clean_df(df, max_characters=200) # long posts break the TTS model

    save_title_and_comments(title, df, 'eleven_labs', idx)

if __name__ == "__main__":
    main()
