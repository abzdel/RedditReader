import sys
from data_handler import read_data, convert_json_to_df, get_title, get_author, clean_df
from file_manager import save_title_and_comments, save_screenshot
import csv
import os
import pandas as pd


def append_to_csv(
    post_id, title, num_comments, voice, tts_method, output_path, subreddit
):
    # Specify the file path
    file_path = f"{output_path}/data.csv"

    # Define the row to be added with default values for null fields
    new_row = {
        "post_id": post_id,
        "title": title,
        "generation_date": None,
        "num_comments": num_comments,
        "uploaded": False,  # false, since not uploaded yet
        "uploaded_date": None,
        "voice_model": voice,
        "tts_method": tts_method,
        "subreddit": None,
        "bg_video": None,
    }

    # Open the CSV file in append mode ('a') and write the new row
    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_row.keys())

        # Check if the CSV is empty to write the header
        if f.tell() == 0:
            writer.writeheader()  # write header only if the file is empty

        # Write the new row
        writer.writerow(new_row)


# function to open up data.csv and pop out any duplicate posts
def check_for_duplicates(csv_output_path, title_id):
    # Specify the file path for the CSV
    file_path = f"{csv_output_path}/data.csv"

    # Load the existing CSV file into a DataFrame
    try:
        existing_df = pd.read_csv(file_path, encoding="ISO-8859-1")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return  # TODO maybe exit?

    # Create a new DataFrame with only the duplicate rows
    if title_id in existing_df["post_id"].values:
        return True


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

    # get subreddit from command line optional
    if len(sys.argv) > 3:
        subreddit = sys.argv[3]
    else:
        subreddit = None

    # if no idx is provided, set it to 0
    if not idx:
        idx = 0

    # arv3 is csv_output_path
    csv_output_path = sys.argv[3]

    # Get data and process
    data = read_data(url)
    title, title_id = get_title(data)

    # check for duplicates
    if check_for_duplicates(csv_output_path, title_id):
        print(f"'{title}' already found. Skipping.")
        return

    df = convert_json_to_df(data)
    df = clean_df(df, max_characters=300)  # long posts break the TTS model

    # save title_id to a text file in outputs/post directory
    # create if not exists
    output_path = f"outputs/post_{idx}/"
    if not os.path.exists(f"outputs/post_{idx}/"):
        os.makedirs(f"outputs/post_{idx}/")

    with open(f"{output_path}/title_id.txt", "w") as f:
        f.write(title_id)
        print(f"Saved title_id to {output_path}/title_id.txt")

    voice_model = "eleven_multilingual_v2"
    voice = "pqHfZKP75CvOlQylNhV4"
    tts_method = "eleven_labs"
    num_comments = 3
    save_title_and_comments(
        title=title,
        df=df,
        model=tts_method,
        idx=idx,
        model_id=voice_model,
        num_comments=num_comments,
        voice=voice,
    )
    save_screenshot(title, get_author(data), idx, output_path)
    print(f"-----FINISHED PROCESSING POST: {title}-----")

    # log data
    append_to_csv(
        post_id=title_id,
        title=title,
        num_comments=num_comments,
        voice=voice,
        tts_method=tts_method,
        output_path=csv_output_path,
        subreddit=subreddit,
    )


if __name__ == "__main__":
    main()
