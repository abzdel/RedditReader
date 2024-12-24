import sys
import shutil

# from data_handler import read_data, convert_json_to_df, get_title, get_author, clean_df
from praw_data_handler import (
    read_data,
    convert_json_to_df,
    get_title,
    get_author,
    clean_df,
)
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
        "subreddit": subreddit,
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

    print(f"Saved '{title}' to {file_path}.")


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

    csv_output_path = sys.argv[4]

    # Get data and process
    data = read_data(url)

    # Move this check before creating any directories
    if data is None:
        print("Skipping post due to invalid data or over_18 content")
        sys.exit(1)  # Exit before creating directory

    # get title
    title, title_id = get_title(data)

    # check for duplicates
    if check_for_duplicates(csv_output_path, title_id):
        print(f"'{title}' already found. Skipping.")
        sys.exit(1)  # Exit before creating directory

    df = convert_json_to_df(data)
    df = clean_df(df, max_characters=300)

    # Clear everything in the outputs folder
    if os.path.exists("outputs"):
        for filename in os.listdir("outputs"):
            file_path = os.path.join("outputs", filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    # Only create directory after all checks pass
    output_path = f"outputs/post_{idx}/"
    if not os.path.exists(f"outputs/post_{idx}/"):
        os.makedirs(f"outputs/post_{idx}/")

        

    with open(f"{output_path}/title_id.txt", "w") as f:
        f.write(title_id)
        print(
            f"Saved title_id to {output_path}/title_id.txt for {title} with idx {idx}"
        )

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
    save_screenshot(title, subreddit, idx, output_path)
    print(f"SAVED SCREENSHOT for {title} with idx {idx}")
    # print(f"-----FINISHED PROCESSING POST: {title}-----")

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
