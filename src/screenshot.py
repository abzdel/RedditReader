import praw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import os
import re


def extract_post_id(reddit_url):
    # Regex pattern to capture post ID in both standard and shortened URLs
    match = re.search(r"(?:comments/|redd\.it/)([a-zA-Z0-9]+)", reddit_url)

    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Reddit URL")


if __name__ == "__main__":
    url = "https://www.reddit.com/r/AskReddit/comments/1fgev2j/what_is_the_best_book_you_have_ever_read/"
    post_id = extract_post_id(url)

    # Set up PRAW
    reddit = praw.Reddit(
        client_id="CLIENT_ID", client_secret="CLIENT_SECRET", user_agent="USER_AGENT"
    )

    # Fetch a Reddit post
    post = reddit.submission(
        id=post_id
    )  # Replace 'POST_ID' with the ID of the Reddit post you want to fetch
    title = post.title

    # Set up Selenium
    service = Service("path/to/chromedriver")
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Create a simple HTML page with the title
    html_content = f"""
    <html>
    <head><title>Reddit Post Title</title></head>
    <body><h1>{title}</h1></body>
    </html>
    """

    # Write HTML to a file
    with open("post_title.html", "w") as file:
        file.write(html_content)

    # Open the HTML file and take a screenshot
    driver.get("file://" + os.path.abspath("post_title.html"))
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))
    image.save("post_title_screenshot.png")

    driver.quit()
