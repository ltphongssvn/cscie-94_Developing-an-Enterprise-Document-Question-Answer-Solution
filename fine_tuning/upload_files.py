# fine_tuning/upload_files.py
# Upload training and validation files to Azure OpenAI

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Upload files
files_to_upload = [
    "fine_tuning/data/train_rice_thai_5pct.jsonl",
    "fine_tuning/data/validation_rice_thai_5pct.jsonl",
]

file_ids = {}
for file_path in files_to_upload:
    print(f"Uploading {file_path}...")
    with open(file_path, "rb") as f:
        result = client.files.create(file=f, purpose="fine-tune")
    file_ids[file_path] = result.id
    print(f"  File ID: {result.id}")

print("\nFile IDs saved:")
for path, fid in file_ids.items():
    print(f"{path}: {fid}")
