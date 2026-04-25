from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import uvicorn
import os
import traceback
from dotenv import load_dotenv

# Load environment variables from .env
import pathlib
# Explicitly load root .env (works regardless of CWD)
_env_path = pathlib.Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)

# Lazy-load AI pipeline
_run_pipeline = None
def get_pipeline():
    global _run_pipeline
    if _run_pipeline is None:
        from main_assistant import run_pipeline
        _run_pipeline = run_pipeline
    return _run_pipeline

from docs_html import DOCS_HTML

# Initialize FastAPI with all essential documentation routes
app = FastAPI(
    title="HCLTech Agentic AI API",
    docs_url="/docs", 
    redoc_url="/redoc", 
    openapi_url="/openapi.json"
)

# Allow Next.js frontend (port 3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.get("/healthz")
async def health():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        pipeline = get_pipeline()
        response_text = pipeline(request.query, history=request.history)
        return ChatResponse(reply=response_text, confidence=0.9)  # type: ignore
    except Exception as e:
        tb = traceback.format_exc()
        print(f"API Error [{type(e).__name__}]: {repr(e)}\n{tb}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {repr(e)}")



if __name__ == "__main__":
    port_env = os.environ.get("PORT", "8000")
    try:
        port = int(port_env)
    except ValueError:
        print(f"WARNING: Invalid PORT environment variable: '{port_env}'. Falling back to 8000.")
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
