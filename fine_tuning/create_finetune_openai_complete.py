# fine_tuning/create_finetune_openai_complete.py
# Complete OpenAI fine-tuning implementation
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: No OPENAI_API_KEY in .env")
    print("\nTo get OpenAI API key:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Create new secret key")
    print("3. Add to .env: OPENAI_API_KEY=sk-...")
    print("4. Run: python fine_tuning/upload_to_openai.py")
    print("5. Then run this script again")
    exit(1)

client = OpenAI(api_key=api_key)

# Replace with IDs from upload_to_openai.py output
training_file = "file-JcBJuUfiJdK5Foz1RfrSeZ"
validation_file = "file-VXAvLARHnMibkcwxBfb6KZ"

if "REPLACE" in training_file:
    print("Run upload_to_openai.py first to get file IDs")
    exit(1)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file,
    validation_file=validation_file,
    model="gpt-3.5-turbo-0125",  # Latest OpenAI model for fine-tuning
    suffix="rice-thai-5pct",
)

print(f"Fine-tuning job created: {job.id}")
print(f"Status: {job.status}")
print(f"Check status: client.fine_tuning.jobs.retrieve('{job.id}')")
