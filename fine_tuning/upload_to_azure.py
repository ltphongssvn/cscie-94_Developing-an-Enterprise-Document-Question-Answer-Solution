# fine_tuning/upload_to_azure.py
# Upload files to Azure OpenAI for fine-tuning
import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

files = [
    "fine_tuning/data/train_rice_thai_5pct.jsonl",
    "fine_tuning/data/validation_rice_thai_5pct.jsonl",
]

file_ids = {}

for file_path in files:
    print(f"Uploading {file_path}...")

    with open(file_path, "rb") as f:
        files_dict = {"file": (os.path.basename(file_path), f, "application/json")}

        response = requests.post(
            f"{endpoint}openai/files?api-version={api_version}",
            headers={"api-key": api_key},
            files=files_dict,
            data={"purpose": "fine-tune"},
        )

    if response.status_code in [200, 201]:  # Both are success codes
        result = response.json()
        file_ids[file_path] = result["id"]
        print(f"  File ID: {result['id']}")
    else:
        print(f"  Error {response.status_code}: {response.text}")
        exit(1)

print("\nFile IDs:")
for path, fid in file_ids.items():
    print(f"{path}: {fid}")
