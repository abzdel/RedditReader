import requests
import replicate
import os

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def narrate_text(text: str, filename: str):
    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    ensure_directory_exists(output_dir)

    file_path = os.path.join(output_dir, filename)

    api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
    output = api.run(
    "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
    input={
        "prompt": text,
        "text_temp": 0.9,
        "output_full": False,
        "waveform_temp": 0.3,
        "history_prompt": "announcer"
    }
        )
    
    # Debugging print
    print(f"Prediction output URL: {output}")

    url = output.get('audio_out')
    if not url:
        raise ValueError("No URL returned from prediction output.")

    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download file.")
