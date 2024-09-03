import requests
import replicate
import os
import json
from io import BytesIO

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def narrate_text_eleven_labs(text: str, filename: str):
    output_dir = os.path.join(os.path.dirname(__file__), 'outputs/')
    ensure_directory_exists(output_dir)

    # Define constants for the script
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
    XI_API_KEY = os.getenv('ELEVEN_LABS_API_TOKEN')
    VOICE_ID = "pqHfZKP75CvOlQylNhV4"  # ID of the voice model to use
    TEXT_TO_SPEAK = text  # Text you want to convert to speech
    OUTPUT_PATH = output_dir + filename  # Path to save the output audio file

    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": TEXT_TO_SPEAK,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)

def narrate_text_tortoise(text: str, filename: str):
    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    ensure_directory_exists(output_dir)
    file_path = os.path.join(output_dir, filename)

    # get voice
    voice = "https://drive.google.com/uc?export=download&id=1xmUwn0L860DuzbuG6r4XBRBw3VSDFiM5"
    mp3_data = load_mp3_from_url(voice)

    api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
    output = api.run(
    "afiaka87/tortoise-tts:e9658de4b325863c4fcdc12d94bb7c9b54cbfe351b7ca1b36860008172b91c71",
    input={
        "seed": 0,
        "text": text,
        "preset": "high_quality", # high_quality, fast
        "voice_a": "custom_voice",
        "voice_b": "disabled",
        "voice_c": "disabled",
        "cvvp_amount": 0,
        "custom_voice": "https://replicate.delivery/mgxm/671f3086-382f-4850-be82-db853e5f05a8/nixon.mp3"
        #"custom_voice": mp3_data

    }
        )

    print(output)
    
    # Debugging print
    print(f"Prediction output URL: {output}")

    url = output
    if not url:
        raise ValueError("No URL returned from prediction output.")

    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download file.")


def load_mp3_from_url(url):
    # Send a GET request to the provided URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    
    # Load the content into a BytesIO object
    mp3_data = BytesIO(response.content)
    return mp3_data