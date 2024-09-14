from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from PIL import Image
from io import BytesIO

# Function to ensure the directory exists
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to capture a screenshot of the Reddit post title
def capture_screenshot(url: str, idx: int):
    # Set up options for headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Provide path to chromedriver
    chrome_driver_path = 'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'
    service = Service(chrome_driver_path)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to the URL
        driver.get(url)
        
        # Check for bot detection page
        if "whoa there" in driver.page_source.lower():
            print("Bot detection page encountered. Exiting.")
            return
        
        # Wait for the title element to be present
        wait = WebDriverWait(driver, 10)
        title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
        
        # Capture screenshot of the entire page
        screenshot = driver.get_screenshot_as_png()
        
        # Load the screenshot into PIL
        image = Image.open(BytesIO(screenshot))
        
        # Get the element's position and size
        location = title_element.location
        size = title_element.size
        
        # Calculate the coordinates of the element
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        
        # Crop the screenshot to the element's bounding box
        image = image.crop((left, top, right, bottom))
        
        # Ensure the output directory exists
        output_directory = f'screenshots/post_{idx}'
        ensure_directory_exists(output_directory)
        
        # Save the screenshot
        screenshot_path = os.path.join(output_directory, 'screenshot.png')
        image.save(screenshot_path)
        
        print(f"Screenshot saved to {screenshot_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Clean up and close the WebDriver
        driver.quit()

# Example usage
if __name__ == "__main__":
    reddit_url = 'https://www.reddit.com/r/AskReddit/comments/1fgev2j/what_is_the_best_book_you_have_ever_read/'
    element_selector = 'shreddit-post'  # Adjust this selector based on the actual element
    capture_screenshot(reddit_url, idx=0)
