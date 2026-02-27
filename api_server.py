from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Any
import uvicorn
import os
import json

# Lazy-load the heavy AI pipeline so the docs route works even if models are still loading
_run_pipeline = None

def get_pipeline():
    global _run_pipeline
    if _run_pipeline is None:
        from main_assistant import run_pipeline
        _run_pipeline = run_pipeline
    return _run_pipeline

# Import the HTML documentation template
from docs_html import DOCS_HTML

app = FastAPI(
    title="HCLTech Agentic AI API",
    description="Enterprise-grade AI assistant for HCLTech with intent detection, RAG, and smart actions.",
    version="1.0.0",
)

class ChatRequest(BaseModel):
    query: str
    user: Optional[str] = "User"
    history: Optional[List[Any]] = []

class ChatResponse(BaseModel):
    reply: str
    metadata: Optional[dict] = {}
    confidence: Optional[float] = 1.0

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/documentation", response_class=HTMLResponse, include_in_schema=False)
async def get_documentation():
    """Serves the beautiful HTML project documentation page."""
    return HTMLResponse(content=DOCS_HTML)

@app.get("/health", tags=["System"])
async def health():
    """Check if the API server is running."""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Send a message to the HCLTech Agentic AI assistant.
    
    - **query**: The user's question or action request
    - **user**: Optional username (default: 'User')  
    - **history**: Optional conversation history for context
    """
    try:
        pipeline = get_pipeline()
        response_text = pipeline(request.query, history=request.history)
        return ChatResponse(
            reply=response_text,
            metadata={},
            confidence=0.9
        )
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
