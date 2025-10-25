# fine_tuning/test_model.py
# Test fine-tuned rice price forecasting model

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test prediction
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal:rice-thai-5pct:CUYRbTTT",
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

print(f"Predicted price: {response.choices[0].message.content}")
