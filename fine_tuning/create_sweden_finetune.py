# fine_tuning/create_sweden_finetune.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

payload = {
    "model": "gpt-35-turbo-0125",
    "training_file": "file-fcb3da4026a041c6b80cd06ae64a94f7",
    "validation_file": "file-4804c86a3ab243e5bd55a69831eb1c40",
    "suffix": "rice-thai-5pct-azure",
    "hyperparameters": {
        "n_epochs": 3,
        "batch_size": 1,
        "learning_rate_multiplier": 1.0,
    },
}

response = requests.post(
    f"{os.getenv('AZURE_OPENAI_ENDPOINT_SWEDEN')}openai/fine_tuning/jobs?api-version={os.getenv('AZURE_OPENAI_API_VERSION')}",
    headers={
        "api-key": os.getenv("AZURE_OPENAI_KEY_SWEDEN"),
        "Content-Type": "application/json",
    },
    json=payload,
)

result = response.json()
print(f"Job ID: {result.get('id', 'N/A')}")
print(f"Status: {result.get('status', 'N/A')}")
print(f"Model: {result.get('model', 'N/A')}")
print(f"\nFull: {result}")
