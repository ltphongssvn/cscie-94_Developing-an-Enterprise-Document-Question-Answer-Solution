# fine_tuning/data/csv_to_jsonl.py
# Converts rice market CSV to JSONL format for Azure OpenAI fine-tuning

import pandas as pd
import json


def create_forecasting_prompt(row, target_col):
    """Create conversational format for price forecasting."""
    features = {
        "date": row["Date"],
        "oil_price": row["Oil_Dubai_Oman_USD_per_bbl"],
        "inflation": row["Inflation_Asia_Avg_pct"],
        "population_growth": row["Population_Growth_Asia_Avg_pct"],
        "enso_anomaly": row["ENSO_Nino34_Anomaly"],
        "enso_phase": row["ENSO_Phase"],
        "fertilizer_price": row["Fertilizer_Composite_USD_per_mt"],
        "rainfall": row["Asia_Avg_Rainfall_mm"],
    }

    user_msg = f"Forecast {target_col.replace('_', ' ')} for {features['date']} given: Oil=${features['oil_price']:.2f}/bbl, Inflation={features['inflation']:.2f}%, ENSO={features['enso_phase']} ({features['enso_anomaly']:.2f}), Fertilizer=${features['fertilizer_price']:.2f}/mt, Rainfall={features['rainfall']:.2f}mm"

    assistant_msg = f"{row[target_col]:.2f}"

    return {
        "messages": [
            {
                "role": "system",
                "content": "You are a rice price forecasting model trained on historical market data.",
            },
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg},
        ]
    }


# Load CSV
df = pd.read_csv("rice_market_optimized_forecasting_20251014_110206.csv")

# Target columns
targets = ["Rice_Thai_5pct", "Rice_Thai_25pct", "Rice_Thai_A1", "Rice_Vietnamese_5pct"]

# Generate JSONL for each target
for target in targets:
    jsonl_data = []
    for _, row in df.iterrows():
        jsonl_data.append(create_forecasting_prompt(row, target))

    # Split: 80% train, 20% validation
    split_idx = int(len(jsonl_data) * 0.8)
    train_data = jsonl_data[:split_idx]
    val_data = jsonl_data[split_idx:]

    # Write training file
    train_file = f"fine_tuning/data/train_{target.lower()}.jsonl"
    with open(train_file, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    # Write validation file
    val_file = f"fine_tuning/data/validation_{target.lower()}.jsonl"
    with open(val_file, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")

    print(f"{target}: {len(train_data)} training, {len(val_data)} validation examples")

print("\nConversion complete!")
