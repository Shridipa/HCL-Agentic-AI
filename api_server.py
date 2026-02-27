"""
HCLTech Agentic AI — FastAPI Backend
=====================================
A professional, enterprise-grade API server with:
- Full OpenAPI/Swagger documentation
- Custom branded ReDoc & Swagger UI pages
- Exported OpenAPI JSON schema
- Lazy-loaded AI pipeline for fast startup
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from enum import Enum
import uvicorn
import os
import json

# ──────────────────────────────────────────────
# Lazy-load the heavy AI pipeline
# ──────────────────────────────────────────────
_run_pipeline = None

def get_pipeline():
    global _run_pipeline
    if _run_pipeline is None:
        from main_assistant import run_pipeline
        _run_pipeline = run_pipeline
    return _run_pipeline

# Import the HTML documentation template
from docs_html import DOCS_HTML

# ──────────────────────────────────────────────
# API Metadata & Description (Markdown supported)
# ──────────────────────────────────────────────
API_TITLE = "HCLTech Agentic AI API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
# 🚀 HCLTech Enterprise Agentic AI Assistant

A **modular, enterprise-grade** AI system designed to handle complex corporate intents — from retrieving financial insights to executing internal actions.

---

## 🔑 Key Capabilities

| Capability | Description |
|---|---|
| **Intent Detection** | Zero-Shot classification using DistilBART-MNLI |
| **RAG Engine** | FAISS + SentenceTransformers for document retrieval |
| **Action Agent** | Generates structured JSON for Jira, Outlook, IAM |
| **Smart Memory** | Context-aware entity scoping across conversations |
| **Guardrails** | Confidence thresholds, citation enforcement, escalation |

## 📡 Supported Intents

- `ask_finance` — Revenue, growth, strategy queries
- `ask_hr` — HR policies, headcount, benefits
- `action_ticket` — IT support ticket creation
- `action_access` — Application access requests
- `action_schedule` — Meeting scheduling

## 🛡️ Architecture

```
User Query → Intent Detection → Sentiment Analysis → Entity Extraction
           → RAG / Policy Check → Response Generation → Action Payload
```

---

> **Built for the HCLTech NLP Challenge** | Powered by FastAPI, Transformers & FAISS
"""

# ──────────────────────────────────────────────
# Tags for organizing endpoints in docs
# ──────────────────────────────────────────────
tags_metadata = [
    {
        "name": "Chat",
        "description": "Core AI assistant interaction endpoints. Send queries and receive intelligent responses.",
    },
    {
        "name": "System",
        "description": "Health checks, version info, and system status endpoints.",
    },
    {
        "name": "Documentation",
        "description": "Custom branded documentation pages and OpenAPI schema export.",
    },
]

# ──────────────────────────────────────────────
# FastAPI App Initialization
# ──────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    openapi_tags=tags_metadata,
    contact={
        "name": "HCLTech Agentic AI Team",
        "url": "https://github.com/Shridipa/HCL-Agentic-AI",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # Disable default docs so we can serve custom branded versions
    docs_url=None,
    redoc_url=None,
)

# ──────────────────────────────────────────────
# CORS Middleware
# ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ══════════════════════════════════════════════
#              PYDANTIC MODELS
# ══════════════════════════════════════════════

class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    query: str = Field(
        ...,
        description="The user's question or action request in natural language.",
        example="What was the revenue growth in FY25?"
    )
    user: Optional[str] = Field(
        default="User",
        description="Optional username for personalization.",
        example="Shridipa"
    )
    history: Optional[List[Any]] = Field(
        default=[],
        description="Previous conversation turns for multi-turn context. Each item should have 'role' and 'content' keys.",
        example=[
            {"role": "user", "content": "Tell me about HCLTech revenue"},
            {"role": "assistant", "content": "HCLTech reported strong growth..."}
        ]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What was the revenue growth in FY25?",
                "user": "Shridipa",
                "history": []
            }
        }

class ChatResponse(BaseModel):
    """Response from the AI assistant."""
    reply: str = Field(
        ...,
        description="The assistant's response text, formatted with markdown."
    )
    metadata: Optional[dict] = Field(
        default={},
        description="Additional metadata about the response (intent, entities, etc.)."
    )
    confidence: Optional[float] = Field(
        default=1.0,
        description="Confidence score of the response (0.0 to 1.0).",
        ge=0.0,
        le=1.0
    )

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Server status", example="healthy")
    version: str = Field(..., description="API version", example="1.0.0")
    modules: dict = Field(..., description="Status of loaded modules")

class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str = Field(..., description="Error description")

# ══════════════════════════════════════════════
#         CUSTOM OPENAPI SCHEMA
# ══════════════════════════════════════════════

def custom_openapi():
    """Generate a custom OpenAPI schema with enhanced metadata."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
        tags=tags_metadata,
    )
    
    # Add custom branding to the schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.hcltech.com/themes/custom/flavor/images/hcltech-logo-white.svg",
        "altText": "HCLTech Logo"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ══════════════════════════════════════════════
#      CUSTOM BRANDED DOCUMENTATION ROUTES
# ══════════════════════════════════════════════

CUSTOM_CSS = """
body { font-family: 'Inter', 'Segoe UI', sans-serif !important; }
.swagger-ui .topbar { background-color: #0f172a !important; }
.swagger-ui .topbar .download-url-wrapper .select-label span { color: #94a3b8 !important; }
.swagger-ui .info .title { color: #6366f1 !important; }
.swagger-ui .scheme-container { background: #1e293b !important; }
"""

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    """
    Custom branded Swagger UI documentation.
    Serves an interactive API playground with HCLTech branding.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{API_TITLE} — Swagger UI",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        # You can host these locally for offline access:
        # swagger_js_url="/static/swagger-ui-bundle.js",
        # swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    """
    Custom branded ReDoc documentation.
    Serves a clean, readable API reference with HCLTech branding.
    """
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{API_TITLE} — ReDoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        # Host locally for offline access:
        # redoc_js_url="/static/redoc.standalone.js",
    )

# ══════════════════════════════════════════════
#         PROJECT DOCUMENTATION PAGE
# ══════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/documentation", response_class=HTMLResponse, tags=["Documentation"],
         summary="Project Documentation",
         description="Serves the full HTML project documentation with architecture, features, and tech stack details.")
async def get_documentation():
    """Serves the beautiful HTML project documentation page."""
    return HTMLResponse(content=DOCS_HTML)

# ══════════════════════════════════════════════
#          OPENAPI SCHEMA EXPORT
# ══════════════════════════════════════════════

@app.get("/openapi.json", tags=["Documentation"],
         summary="Export OpenAPI Schema",
         description="Returns the raw OpenAPI 3.x JSON schema. Use this with external tools like Swagger Codegen, Redocly CLI, or Postman to generate client SDKs or static documentation.",
         response_class=JSONResponse)
async def export_openapi_schema():
    """
    Export the full OpenAPI schema as JSON.
    
    **Use cases:**
    - Import into **Postman** for API testing
    - Generate **client SDKs** with Swagger Codegen
    - Build **static HTML docs** with Redocly CLI
    - Share with team members for integration
    """
    return JSONResponse(content=app.openapi())

# ══════════════════════════════════════════════
#              SYSTEM ENDPOINTS
# ══════════════════════════════════════════════

@app.get("/health", tags=["System"],
         response_model=HealthResponse,
         summary="Health Check",
         description="Returns the current health status of the API server and its loaded modules.")
async def health():
    """Check if the API server and its modules are operational."""
    modules_status = {
        "fastapi": "loaded",
        "docs_html": "loaded",
        "ai_pipeline": "loaded" if _run_pipeline is not None else "lazy (not yet loaded)",
    }
    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        modules=modules_status
    )

@app.get("/version", tags=["System"],
         summary="Version Info",
         description="Returns detailed version and configuration information.")
async def version_info():
    """Get version details and configuration."""
    return {
        "api_version": API_VERSION,
        "title": API_TITLE,
        "python_backend": "FastAPI + Uvicorn",
        "ai_models": {
            "generator": "google/flan-t5-base",
            "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
            "classifier": "valhalla/distilbart-mnli-12-1"
        },
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health",
            "swagger_docs": "/docs",
            "redoc_docs": "/redoc",
            "documentation": "/documentation",
            "openapi_schema": "/openapi.json"
        }
    }

# ══════════════════════════════════════════════
#              CHAT ENDPOINT
# ══════════════════════════════════════════════

@app.post("/api/chat",
          response_model=ChatResponse,
          responses={
              200: {"description": "Successful AI response", "model": ChatResponse},
              500: {"description": "Internal server error", "model": ErrorResponse},
          },
          tags=["Chat"],
          summary="Chat with the AI Assistant",
          description="""
Send a natural language query to the HCLTech Agentic AI assistant. 
The system will automatically:

1. **Detect intent** (finance, HR, IT ticket, scheduling, etc.)
2. **Extract entities** (employee ID, dates, departments)
3. **Retrieve context** from the knowledge base via RAG
4. **Generate a response** or create an action payload

Supports multi-turn conversations via the `history` parameter.
""")
async def chat(request: ChatRequest):
    """
    Main AI chat endpoint. Processes the user query through the full
    agentic pipeline: Intent → NER → RAG → Policy → Response.
    """
    try:
        pipeline = get_pipeline()
        response_text = pipeline(request.query, history=request.history)
        return ChatResponse(
            reply=response_text,
            metadata={
                "user": request.user,
                "query_length": len(request.query),
                "history_turns": len(request.history) if request.history else 0
            },
            confidence=0.9
        )
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ══════════════════════════════════════════════
#              RUN SERVER
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   🚀 {API_TITLE}               ║
    ║   Version: {API_VERSION}                           ║
    ╠══════════════════════════════════════════════╣
    ║   Documentation:  http://localhost:8000/     ║
    ║   Swagger UI:     http://localhost:8000/docs ║
    ║   ReDoc:          http://localhost:8000/redoc║
    ║   OpenAPI JSON:   http://localhost:8000/openapi.json
    ║   Health:         http://localhost:8000/health
    ╚══════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
