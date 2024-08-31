import requests
import replicate

def narrate_text(text: str, filename: str):
    deployment = replicate.deployments.get("abzdel/default-text-to-speech")
    prediction = deployment.predictions.create(input={"text": text})
    prediction.wait()
    
    url = prediction.output
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(f'outputs/{filename}', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download file.")
