import sys
from data_handler import read_data, convert_json_to_df, get_title, get_author, clean_df
from file_manager import save_title_and_comments, save_screenshot
import csv


def append_to_csv(post_id, title, num_comments, voice_model, tts_method, output_path):
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
        "voice_model": voice_model,
        "tts_method": tts_method,
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

    # arv3 is csv_output_path
    csv_output_path = sys.argv[3]

    # Get data and process
    data = read_data(url)
    title, title_id = get_title(data)
    df = convert_json_to_df(data)
    df = clean_df(df, max_characters=300)  # long posts break the TTS model

    # save title_id to a text file in outputs/post directory
    with open(f"outputs/post_{idx}/title_id.txt", "w") as f:
        f.write(title_id)
        print(f"Saved title_id to src/outputs/post_{idx}/title_id.txt")

    voice_model = "eleven_multilingual_v2"
    tts_method = "eleven_labs"
    num_comments = 3
    save_title_and_comments(
        title=title,
        df=df,
        model=tts_method,
        idx=idx,
        model_id=voice_model,
        num_comments=num_comments,
    )
    save_screenshot(title, get_author(data), idx)

    # log data
    append_to_csv(
        post_id=title_id,
        title=title,
        num_comments=num_comments,
        voice_model=voice_model,
        tts_method=tts_method,
        output_path=csv_output_path,
    )


if __name__ == "__main__":
    main()
