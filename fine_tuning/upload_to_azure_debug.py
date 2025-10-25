# fine_tuning/upload_to_azure_debug.py
# Debug version to see actual Azure API response
import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

file_path = "fine_tuning/data/train_rice_thai_5pct.jsonl"
print(f"Uploading {file_path}...")
print(f"Full URL: {endpoint}openai/files?api-version={api_version}")

with open(file_path, "rb") as f:
    response = requests.post(
        f"{endpoint}openai/files?api-version={api_version}",
        headers={"api-key": api_key},
        files={"file": f},
        data={"purpose": "fine-tune"},
    )

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Body: {response.text}")
