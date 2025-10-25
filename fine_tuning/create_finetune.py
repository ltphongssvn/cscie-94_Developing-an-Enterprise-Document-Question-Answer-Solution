# fine_tuning/create_finetune.py
# Create fine-tuning job for rice price forecasting

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file="file-b69f759da0bf4e7a896b48aad1f19ef4",
    validation_file="file-a28eb924750047278216018d47c44661",
    model="gpt-35-turbo-1106",
    suffix="rice-thai-5pct",
)

print(f"Fine-tuning job created: {job.id}")
print(f"Status: {job.status}")
print(f"Model: {job.model}")
