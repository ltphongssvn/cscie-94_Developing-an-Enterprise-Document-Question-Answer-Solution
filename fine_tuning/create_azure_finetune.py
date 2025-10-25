# fine_tuning/create_azure_finetune.py
# Create Azure OpenAI fine-tuning job with LoRA and hyperparameters

import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# LoRA is used automatically by Azure OpenAI for efficiency
payload = {
    "model": "gpt-35-turbo-0125",
    "training_file": "file-d1c74ff781bc4460adca8f6bd429cc4f",
    "validation_file": "file-25fd36d5dd6b4190a2363c5e2c5b976d",
    "suffix": "rice-thai-5pct-azure",
    "hyperparameters": {
        "n_epochs": 3,
        "batch_size": 1,
        "learning_rate_multiplier": 1.0,
    },
}

response = requests.post(
    f"{endpoint}openai/fine_tuning/jobs?api-version={api_version}",
    headers={"api-key": api_key, "Content-Type": "application/json"},
    json=payload,
)

result = response.json()
print(f"Job ID: {result.get('id', 'N/A')}")
print(f"Status: {result.get('status', 'N/A')}")
print(f"Model: {result.get('model', 'N/A')}")
print(f"\nFull response: {result}")
