# fine_tuning/create_finetune_openai.py
# Alternative fine-tuning using OpenAI direct (not Azure)
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Check for OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    print("Get your key from: https://platform.openai.com/api-keys")
    print("Add to .env: OPENAI_API_KEY=sk-...")
    exit(1)

client = OpenAI(api_key=api_key)

# Note: Files need to be re-uploaded to OpenAI platform
print("This script requires uploading files to OpenAI platform.")
print("Your current files are on Azure and need re-uploading.")
print("Add OPENAI_API_KEY to .env first, then re-run upload scripts.")
