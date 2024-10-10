from PIL import Image, ImageDraw, ImageFont
import os

# Filepath to the base image
BASE_IMAGE_PATH = "../reddit_template.jfif"
OUTPUT_IMAGE_PATH = "TEST_IMAGE.png"

# Default font for text overlay (adjust if needed)
FONT_PATH = "fonts/DejaVuSans-Bold.ttf"  # Adjust path if necessary
FONT_SIZE_USERNAME = 30
FONT_SIZE_TITLE = 36

# Coordinates for text placement
USERNAME_POSITION = (
    165,
    35,
)  # Initial Y position for username (X will be calculated dynamically)
TITLE_POSITION = (65, 150)  # Bottom part of the image


def load_font(font_path, font_size):
    """
    Tries to load the font with the specified size. If it fails, defaults to a built-in font.
    """
    try:
        font = ImageFont.truetype(font_path, font_size)
        return font
    except IOError:
        print("Font file not found, using default font.")
        return ImageFont.load_default()


def load_image(image_path):
    """
    Loads the base image where the post will be overlaid.
    """
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def add_username(image, username):
    """
    Adds the username to the image at the specified location without dynamic positioning.
    """
    draw = ImageDraw.Draw(image)
    font = load_font(FONT_PATH, FONT_SIZE_USERNAME)

    # Add the username at the predefined position (static placement)
    draw.text(
        USERNAME_POSITION, username, font=font, fill=(0, 0, 0)
    )  # Black text at the fixed USERNAME_POSITION
    return image


def add_subreddit(image, subreddit):
    """
    Adds the subreddit to the image at the specified location without dynamic positioning.
    """
    draw = ImageDraw.Draw(image)
    font = load_font(FONT_PATH, FONT_SIZE_USERNAME)

    # Add the subreddit at the predefined position (static placement)
    draw.text(
        USERNAME_POSITION, subreddit, font=font, fill=(0, 0, 0)
    )  # Black text at the fixed USERNAME_POSITION
    return image


def add_post_title(image, post_title):
    """
    Adds the post title to the image at the specified location with text wrapping.
    """
    draw = ImageDraw.Draw(image)
    font = load_font(FONT_PATH, FONT_SIZE_TITLE)

    # Set the maximum width for the title
    max_width = image.size[0] - 100  # Leave some padding on the sides
    lines = []
    words = post_title.split()

    current_line = ""
    for word in words:
        # Check if adding the next word would exceed the max width
        test_line = f"{current_line} {word}".strip()
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = text_bbox[2] - text_bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            # Add the current line to lines and start a new line with the word
            lines.append(current_line)
            current_line = word

    # Add the last line if it exists
    if current_line:
        lines.append(current_line)

    # Get the height of the font
    line_height = (
        draw.textbbox((0, 0), "Hg", font=font)[3]
        - draw.textbbox((0, 0), "Hg", font=font)[1]
    )  # Estimate height

    # Draw each line of the title on the image
    for i, line in enumerate(lines):
        draw.text(
            (TITLE_POSITION[0], TITLE_POSITION[1] + i * line_height),
            line,
            font=font,
            fill=(0, 0, 0),
        )  # Black text

    return image


def save_image(image, output_path):
    """
    Saves the modified image to the specified path.
    """
    try:
        image.save(output_path)
        print(f"Image saved successfully at {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


def truncate_author(author: str) -> str:
    if len(author) > 20:
        return author[:18] + "..."
    return author


def generate_screenshot(post_title, username, screenshot_path):
    """
    Main function to generate the Reddit-like post image.
    """
    # Parameters for username and post title
    # username = "u/temp"  # You can customize this
    # post_title = "IT workers of Reddit, can companies track all means of copying data from corporate laptops, specifically online syncing like Google Drive or using Air Drop on Mac?"  # Sample post title, replace as needed

    # Load base image from BASE_IMAGE_PATH
    image = load_image(BASE_IMAGE_PATH)
    if image is None:
        return  # Exit if image loading failed

    username = truncate_author(username)
    username = "u/" + username

    # Add username to the image
    image = add_username(image, username)

    # Add post title to the image
    image = add_post_title(image, post_title)

    # Save the final image
    save_image(image, screenshot_path)


def main():
    generate_screenshot("title", "username", "/")


if __name__ == "__main__":
    main()
