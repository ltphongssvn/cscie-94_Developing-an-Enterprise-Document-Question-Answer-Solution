# fine_tuning/rag_alternative.py
# RAG approach instead of fine-tuning - works with Cognitive Services
import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Load training data as context examples
with open("fine_tuning/data/train_rice_thai_5pct.jsonl", "r") as f:
    examples = [json.loads(line) for line in f][:5]  # Use top 5 as few-shot


def predict_with_rag(user_input):
    # Build few-shot prompt with examples
    system_prompt = (
        "You are a rice price forecasting expert. Analyze patterns and predict prices."
    )

    few_shot = "\n".join(
        [
            f"Input: {ex['messages'][1]['content']}\nOutput: {ex['messages'][2]['content']}"
            for ex in examples
            if len(ex["messages"]) > 2
        ]
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Examples:\n{few_shot}\n\nNow predict:\n{user_input}",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-35-turbo", messages=messages, temperature=0.3  # Your deployment name
    )
    return response.choices[0].message.content


# Test
print("RAG-based prediction ready. No fine-tuning needed.")
print("Uses few-shot learning with your training examples.")
