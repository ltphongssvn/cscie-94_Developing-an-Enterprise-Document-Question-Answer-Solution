# fine_tuning/download_results.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

file_id = "file-f0bc4fc7a70b404db67a2d0fed516d65"

response = requests.get(
    f"{os.getenv('AZURE_OPENAI_ENDPOINT_SWEDEN')}openai/files/{file_id}/content?api-version={os.getenv('AZURE_OPENAI_API_VERSION')}",
    headers={"api-key": os.getenv("AZURE_OPENAI_KEY_SWEDEN")},
)

with open("fine_tuning/results.csv", "wb") as f:
    f.write(response.content)

print("Results downloaded to fine_tuning/results.csv")
