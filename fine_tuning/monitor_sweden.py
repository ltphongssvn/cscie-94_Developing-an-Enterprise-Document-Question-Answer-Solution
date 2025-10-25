# fine_tuning/monitor_sweden.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

job_id = "ftjob-383faf4466084382960e84f995123316"

response = requests.get(
    f"{os.getenv('AZURE_OPENAI_ENDPOINT_SWEDEN')}openai/fine_tuning/jobs/{job_id}?api-version={os.getenv('AZURE_OPENAI_API_VERSION')}",
    headers={"api-key": os.getenv("AZURE_OPENAI_KEY_SWEDEN")},
)

result = response.json()
print(f"Status: {result.get('status')}")
print(f"Fine-tuned model: {result.get('fine_tuned_model', 'Not ready')}")
print(f"\nFull: {result}")
