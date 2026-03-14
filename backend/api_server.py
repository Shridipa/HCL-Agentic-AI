from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

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

class ScheduleRequest(BaseModel):
    """Payload sent from the Next.js frontend to trigger calendar+email on meeting confirm."""
    topic: str
    date: Optional[str] = "TBD"
    time: Optional[str] = "TBD"
    location: Optional[str] = "Virtual"
    participants: Optional[Any] = []
    participant_emails: Optional[List[str]] = []
    organizer_email: Optional[str] = ""
    organizer_name: Optional[str] = "Associate"

class ScheduleResponse(BaseModel):
    status: str          # "success" | "partial" | "failed"
    summary: str
    meet_link: Optional[str] = ""
    calendar: Optional[dict] = {}
    email: Optional[dict] = {}

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
        return ChatResponse(reply=response_text, confidence=0.9)  # type: ignore
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule", response_model=ScheduleResponse)
async def schedule_meeting(request: ScheduleRequest):
    """
    Called by the Next.js frontend when the user confirms a schedule_meeting action.
    Creates a Google Calendar event and sends email notifications to all participants.
    """
    print(f"DEBUG: Schedule Request received. Organizer: {request.organizer_email}, Topic: {request.topic}")
    try:
        from calendar_email_service import schedule_and_notify
        action_data = {
            "topic": request.topic,
            "date": request.date,
            "time": request.time,
            "location": request.location,
            "participants": request.participants,
            "participant_emails": request.participant_emails,
        }
        result = schedule_and_notify(
            action_data, 
            organizer_email=request.organizer_email,
            organizer_name=request.organizer_name
        )
        return ScheduleResponse(
            status=result["status"],
            summary=result["summary"],
            meet_link=result.get("meet_link", ""),
            calendar=result.get("calendar", {}),
            email=result.get("email", {}),
        )
    except Exception as e:
        print(f"Schedule API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
