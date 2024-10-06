import sys
from data_handler import read_data, convert_json_to_df, get_title, get_author, clean_df
from file_manager import save_title_and_comments, save_screenshot


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
    df = clean_df(df, max_characters=300)  # long posts break the TTS model

    save_title_and_comments(title, df, "eleven_labs", idx)
    save_screenshot(title, get_author(data), idx)


if __name__ == "__main__":
    main()
