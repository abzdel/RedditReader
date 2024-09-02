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
        "lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e",
            input={"text": text,
                "speaker": "https://replicate.delivery/pbxt/Jt79w0xsT64R1JsiJ0LQRL8UcWspg5J4RFrU6YwEKpOT1ukS/male.wav",
                "cleanup_voice": True}
        )
    
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
