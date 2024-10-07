import pandas as pd
from text_to_speech import *
from generate_screenshot import *
import os


def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_title_and_comments(
    title: str,
    df: pd.DataFrame,
    model: str,
    idx: int = 0,
    model_id="eleven_multilingual_v2",
    num_comments=3,
):
    # Define output directory for the specific post
    output_dir = os.path.join(os.path.dirname(__file__), f"outputs/post_{idx}/")
    ensure_directory_exists(output_dir)

    # Sort and reset the DataFrame (keeping top 3 comments)
    df = df.sort_values(by="score", ascending=False).head(num_comments)
    df = df.reset_index(drop=True)

    if model == "eleven_labs":
        # Process title
        narrate_text_eleven_labs(title, "post_title.mp3", idx, model_id)

        # Process comments
        for comment_idx, row in df.iterrows():
            print(f"Processing comment_{comment_idx} with text: {row['text']}")
            # Here, we pass idx to ensure it's saved in the correct post folder
            narrate_text_eleven_labs(row["text"], f"comment_{comment_idx}.mp3", idx)
    elif model == "tortoise":
        # Process title
        narrate_text_tortoise(title, "post_title.mp3")

        # Process comments
        for comment_idx, row in df.iterrows():
            print(f"Processing comment_{comment_idx} with text: {row['text']}")
            narrate_text_tortoise(row["text"], f"comment_{comment_idx}.mp3")
    else:
        raise Exception(
            f"Model {model} not supported or mistyped. Please use 'eleven_labs' or 'tortoise'."
        )
    print(f"-----FINISHED PROCESSING POST: {title}-----")


def save_screenshot(title: str, author: str, idx: int):
    # Define the output directory for the specific post
    output_dir = os.path.join(os.path.dirname(__file__), f"outputs/post_{idx}/")

    # Define the screenshot filename
    screenshot_filename = "title_screenshot.png"

    # Go up one directory level to check for the existing image
    parent_dir = os.path.dirname(output_dir)
    existing_image_path = os.path.join(parent_dir, screenshot_filename)

    # Check if the image already exists in the parent directory
    if os.path.isfile(existing_image_path):
        print(f"Image already exists: {existing_image_path}")
        return existing_image_path  # Return the existing image path if found

    # Define the path to save the new screenshot
    screenshot_path = os.path.join(output_dir, screenshot_filename)

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Call the generate_screenshot function and save the result
    generate_screenshot(title, author, screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    return screenshot_path  # Return the path where the screenshot was saved
