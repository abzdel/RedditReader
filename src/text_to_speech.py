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

    deployment = replicate.deployments.get("abzdel/default-text-to-speech")
    prediction = deployment.predictions.create(input={"text": text})
    prediction.wait()
    
    url = prediction.output
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download file.")
