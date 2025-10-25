# backend/api.py
# FastAPI backend for Azure OpenAI fine-tuning UI

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY_SWEDEN"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_SWEDEN"),
)


class PredictionRequest(BaseModel):
    oil: float
    inflation: float
    enso: float
    fertilizer: float
    rainfall: float


@app.get("/api")
def root():
    return {"status": "Azure OpenAI Fine-Tuning API", "deployment": "rice-thai-5pct"}


@app.post("/api/predict")
def predict(req: PredictionRequest):
    try:
        prompt = f"Forecast Rice Thai 5pct given: Oil=${req.oil}/bbl, Inflation={req.inflation}%, ENSO={req.enso}, Fertilizer=${req.fertilizer}/mt, Rainfall={req.rainfall}mm"

        response = client.chat.completions.create(
            model="rice-thai-5pct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a rice price forecasting model trained on historical market data.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        price = response.choices[0].message.content
        return {"prediction": price, "prompt": prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health():
    return {"status": "healthy"}


# Serve React frontend
if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        return FileResponse("frontend/build/index.html")
