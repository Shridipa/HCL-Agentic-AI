from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import uvicorn
import os

# Lazy-load AI pipeline
_run_pipeline = None
def get_pipeline():
    global _run_pipeline
    if _run_pipeline is None:
        from main_assistant import run_pipeline
        _run_pipeline = run_pipeline
    return _run_pipeline

from docs_html import DOCS_HTML

# Initialize FastAPI with all built-in docs disabled
app = FastAPI(
    title="HCLTech Agentic AI API",
    docs_url=None, 
    redoc_url=None, 
    openapi_url=None
)

class ChatRequest(BaseModel):
    query: str
    user: Optional[str] = "User"
    history: Optional[List[Any]] = []

class ChatResponse(BaseModel):
    reply: str
    metadata: Optional[dict] = {}
    confidence: Optional[float] = 1.0

# THE ONLY DOCUMENTATION ROUTE
@app.get("/", response_class=HTMLResponse)
@app.get("/documentation", response_class=HTMLResponse)
async def get_documentation():
    """Serves the single, beautiful HTML project documentation page."""
    return HTMLResponse(content=DOCS_HTML)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        pipeline = get_pipeline()
        response_text = pipeline(request.query, history=request.history)
        return ChatResponse(reply=response_text, confidence=0.9)
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
