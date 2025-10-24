# backend/api.py
# Full path: /backend/api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.document_qa import DocumentQASystem

app = FastAPI(title="Document Q&A API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QA system
qa_system = None


class Query(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: int


@app.on_event("startup")
async def startup_event():
    """Initialize QA system on startup."""
    global qa_system
    qa_system = DocumentQASystem()
    qa_system.setup()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Document Q&A API"}


@app.post("/query", response_model=QueryResponse)
async def query_documents(query: Query):
    """Query the document Q&A system."""
    if not qa_system:
        raise HTTPException(status_code=503, detail="System not initialized")

    try:
        result = qa_system.query(query.question)
        return QueryResponse(
            question=query.question,
            answer=result["result"],
            sources=len(result.get("source_documents", [])),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Detailed health check."""
    return {"status": "healthy", "qa_system_initialized": qa_system is not None}
