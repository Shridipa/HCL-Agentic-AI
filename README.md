# 🧠 HCLTech Agentic AI — Enterprise Assistant

<div align="center">

![HCLTech AI](https://img.shields.io/badge/HCLTech-Agentic%20AI-0066cc?style=for-the-badge&logo=brain&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA--3%2070B-orange?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-blueviolet?style=for-the-badge)

**A production-ready, "Guardrails-First" enterprise AI assistant that retrieves financial intelligence, automates IT workflows, and manages corporate actions — powered by RAG + Groq LLaMA-3.**

[Live Demo](https://drive.google.com/file/d/1XdwsUorYmzm68y7RskkhRKpUF5pRQhIU/view?usp=sharing) • [API Docs](#api-endpoints) • [Setup Guide](#-quick-start)

</div>

---

## 📌 Project Overview

The HCLTech Agentic AI is a full-stack enterprise assistant built for the NLP Challenge. It combines:

- **RAG pipeline** over HCLTech's Annual Report 2024–25 (FAISS + SentenceTransformers)
- **Groq LLaMA-3 70B** for high-speed, grounded answer synthesis
- **Multi-intent detection** (finance, HR, IT, scheduling, access)
- **Agentic actions** — structured JSON output for IT tickets, access requests, meeting scheduling
- **Premium Next.js dashboard** with glass-morphic UI and real-time chat

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │Intent Detect │──▶│ NER Extract  │──▶│Agent Policy│  │
│  │(Groq LLaMA-3)│   │(Groq LLaMA-3)│   │   Layer    │  │
│  └──────────────┘   └──────────────┘   └─────┬──────┘  │
│                                               │         │
│         ┌──────────────────┬─────────────────┤         │
│         ▼                  ▼                 ▼         │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐    │
│   │RAG (FAISS│      │ Action   │      │Clarify / │    │
│   │+ mpnet)  │      │Generator │      │Escalate  │    │
│   └────┬─────┘      └────┬─────┘      └──────────┘    │
│        ▼                 ▼                             │
│   ┌──────────────────────────────┐                    │
│   │  Groq LLaMA-3 Synthesizer    │                    │
│   └──────────────────────────────┘                    │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Next.js Frontend Dashboard (Port 3000)
```

### Backend Modules

| Module | Purpose |
|---|---|
| `api_server.py` | FastAPI entry point — `/api/chat`, `/health`, `/docs` |
| `main_assistant.py` | Orchestrates the full 5-step pipeline |
| `intent_detector.py` | Groq-powered zero-shot intent classification |
| `ner_extractor.py` | Groq-powered named entity extraction |
| `sentiment_analyzer.py` | Urgency & sentiment analysis via Groq |
| `query_assistant.py` | FAISS vector retrieval with RRF re-ranking |
| `agent_policy.py` | Decides: answer / action / clarify / escalate |
| `action_generator.py` | Structured JSON for tickets, access, meetings |
| `clarifier.py` | Generates targeted clarification prompts |
| `citation_enforcer.py` | Validates citations from retrieved chunks |
| `process_pdf.py` | PDF ingestion & chunk creation |
| `index_chunks.py` | Builds FAISS index from chunks |
| `docs_html.py` | In-memory HTML project documentation page |
| `gradio_app.py` | Optional Gradio interface |

### Frontend Pages

| Route | Description |
|---|---|
| `/` | Login page (username + password) |
| `/dashboard` | Main chat interface + Finance, Support, Calendar, Access panels |

---

## ✨ Key Features

### 🎯 Multi-Intent Detection
- **12 intent classes**: `ask_finance`, `ask_hr`, `ask_it_policy`, `ask_compliance`, `ask_security`, `ask_procurement`, `ask_people`, `action_ticket`, `action_access`, `action_schedule`, and more
- Groq LLaMA-3 as primary classifier with keyword-boost fallback
- Multi-turn context stickiness for follow-up queries

### 📚 Enterprise RAG
- HCLTech Annual Report 2024–25 chunked into 500-token segments
- `all-mpnet-base-v2` (768-dim) embeddings → FAISS `IndexFlatL2`
- **Hybrid retrieval**: Semantic similarity + lexical overlap (RRF scoring)
- Section-aware filtering (Financial / HR / Governance / IT)
- Direct Groq fallback for queries with no RAG match

### ⚙️ Agentic Actions
- **IT Ticket** — structured JSON with priority, department, reference ID
- **Access Request** — scoped to application and employee
- **Meeting Scheduling** — extracts topic, date, time, participants

### 🛡️ Guardrails-First Policy
- Confidence thresholding before answer / action decision
- Entity validation against retrieved chunks
- Human escalation trigger for high-urgency / low-confidence cases

### 💎 Premium Dashboard
- Dark glassmorphic Next.js UI (shadcn/ui components)
- Real-time chat with structured JSON response cards
- Finance ledger, Support tickets, Calendar, Access panels
- Persistent local storage for meetings and tickets

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone & Configure

```bash
git clone https://github.com/Shridipa/HCL-Agentic-AI.git
cd HCL-Agentic-AI
```

Create `.env` in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python api_server.py
```

Backend runs at → **http://localhost:8000**

### 3. Frontend Setup

```bash
cd frontend
```

Create `frontend/.env.local`:
```env
ML_MODEL_ENDPOINT=http://localhost:8000/api/chat
GROQ_API_KEY=your_groq_api_key_here
```

```bash
npm install
npm run dev
```

Frontend runs at → **http://localhost:3000**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Interactive project documentation |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc API reference |
| `POST` | `/api/chat` | Main chat endpoint |

### `/api/chat` Payload

```json
{
  "query": "What was HCLTech's revenue growth in FY25?",
  "user": "Alice",
  "history": []
}
```

### Response Schema

```json
{
  "reply": "{\"title\": \"Answer: Revenue Growth\", \"direct_answer\": \"...\", \"key_insights\": [...], \"citations\": [...], \"confidence_score\": \"High\"}",
  "confidence": 0.9
}
```

---

## 💬 Example Queries

| Type | Example |
|---|---|
| Finance | `"What was HCLTech's revenue in FY25?"` |
| People | `"Who is the CEO of HCLTech?"` |
| HR | `"What is the maternity leave policy?"` |
| IT Ticket | `"My laptop screen is flickering, raise a high priority ticket"` |
| Access | `"I need access to the SAP portal"` |
| Scheduling | `"Schedule a meeting with the finance team for next Monday at 10am"` |

---

## 📁 Project Structure

```
HCL-Agentic-AI/
├── .env                          # Root env (GROQ_API_KEY)
├── .gitignore
├── README.md
├── docker-compose.yml
│
├── backend/
│   ├── api_server.py             # FastAPI server
│   ├── main_assistant.py         # Pipeline orchestrator
│   ├── intent_detector.py        # Intent classification
│   ├── ner_extractor.py          # Entity extraction
│   ├── sentiment_analyzer.py     # Sentiment & urgency
│   ├── query_assistant.py        # FAISS retrieval
│   ├── agent_policy.py           # Policy decision layer
│   ├── action_generator.py       # Action JSON builder
│   ├── clarifier.py              # Clarification generator
│   ├── citation_enforcer.py      # Citation validator
│   ├── ui_formatter.py           # Response formatter
│   ├── process_pdf.py            # PDF → chunks
│   ├── index_chunks.py           # Chunks → FAISS index
│   ├── gradio_app.py             # Gradio UI (optional)
│   ├── docs_html.py              # Documentation HTML
│   ├── faq_index.faiss           # Pre-built vector index
│   ├── chunks_mapping.json       # Chunk metadata
│   ├── chunks.json               # Raw chunks
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/
    ├── app/
    │   ├── page.tsx              # Login page
    │   ├── dashboard/page.tsx    # Main dashboard
    │   └── api/chat/route.ts     # Next.js API proxy
    ├── components/ui/            # shadcn/ui components
    ├── public/
    │   ├── avatar.png            # AI avatar
    │   └── docs.html             # Static docs page
    ├── .env.local                # Frontend env vars
    └── package.json
```

---

## 🔮 Roadmap

- [ ] Multi-document RAG (policy docs, IT manuals, FAQs)
- [ ] Persistent conversation history (PostgreSQL / Redis)
- [ ] User authentication with JWT
- [ ] Analytics dashboard (intent frequency, escalation rate)
- [ ] Slack / MS Teams integration
- [ ] Fine-tuned intent classifier on HCLTech domain data

---

## 📄 License

This project was built for the **HCLTech NLP Challenge 2026**.

---

<div align="center">
Built with ❤️ by <strong>Shridipa Dasgupta</strong>
</div>
