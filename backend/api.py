# backend/api.py
# Full path: /backend/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


@app.post("/api/query", response_model=QueryResponse)
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


@app.get("/api/health")
async def health():
    """Detailed health check."""
    return {"status": "healthy", "qa_system_initialized": qa_system is not None}


# Mount static files
frontend_build = "frontend/build"
if os.path.exists(frontend_build):
    app.mount(
        "/static", StaticFiles(directory=f"{frontend_build}/static"), name="static"
    )

    @app.get("/{path:path}")
    async def serve_react_app(path: str):
        # Don't catch API routes
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(frontend_build, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_build, "index.html"))
