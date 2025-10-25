# fine_tuning/upload_to_openai.py
# Upload training files to OpenAI platform
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Add OPENAI_API_KEY=sk-... to .env file first")
    exit(1)

client = OpenAI(api_key=api_key)

# Upload training file
with open("fine_tuning/data/train_rice_thai_5pct.jsonl", "rb") as f:
    train_file = client.files.create(file=f, purpose="fine-tune")
    print(f"Training file uploaded: {train_file.id}")

# Upload validation file
with open("fine_tuning/data/validation_rice_thai_5pct.jsonl", "rb") as f:
    val_file = client.files.create(file=f, purpose="fine-tune")
    print(f"Validation file uploaded: {val_file.id}")

print("\nUpdate create_finetune_openai.py with these IDs:")
print(f'training_file="{train_file.id}"')
print(f'validation_file="{val_file.id}"')
