# fine_tuning/upload_to_sweden.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_SWEDEN")
api_key = os.getenv("AZURE_OPENAI_KEY_SWEDEN")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

files = [
    "fine_tuning/data/train_rice_thai_5pct.jsonl",
    "fine_tuning/data/validation_rice_thai_5pct.jsonl",
]

for file_path in files:
    print(f"Uploading {file_path}...")
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{endpoint}openai/files?api-version={api_version}",
            headers={"api-key": api_key},
            files={"file": (file_path.split("/")[-1], f, "application/jsonl")},
            data={"purpose": "fine-tune"},
        )
    result = response.json()
    print(f"  File ID: {result.get('id', 'ERROR')}")
    if "error" in result:
        print(f"  Error: {result['error']}")
