# fine_tuning/monitor_job.py
# Monitor OpenAI fine-tuning job status
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

job_id = "ftjob-7pc0kvPb7uefsGQif7o1WLm6"
job = client.fine_tuning.jobs.retrieve(job_id)

print(f"Job ID: {job.id}")
print(f"Status: {job.status}")
print(f"Model: {job.model}")
if job.fine_tuned_model:
    print(f"Fine-tuned model: {job.fine_tuned_model}")
if job.error:
    print(f"Error: {job.error}")
print(f"Created: {job.created_at}")
if job.finished_at:
    print(f"Finished: {job.finished_at}")
