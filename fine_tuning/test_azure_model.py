# fine_tuning/test_azure_model.py
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_SWEDEN"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_SWEDEN"),
)

response = client.chat.completions.create(
    model="rice-thai-5pct",
    messages=[
        {
            "role": "system",
            "content": "You are a rice price forecasting model trained on historical market data.",
        },
        {
            "role": "user",
            "content": "Forecast Rice Thai 5pct for 2024-01-01 given: Oil=$80.00/bbl, Inflation=3.50%, ENSO=La Nina (-1.20), Fertilizer=$650.00/mt, Rainfall=180.00mm",
        },
    ],
)

print(f"Predicted: {response.choices[0].message.content}")
