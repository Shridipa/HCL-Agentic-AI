🚀 HCLTech Enterprise Assistant — NLP Challenge

🧠 Project Overview
The HCLTech Enterprise Assistant is a modular, enterprise-grade AI system designed to handle a wide range of corporate intents — from retrieving financial insights from the Annual Report (2024–25) to executing internal actions like IT ticket creation and meeting scheduling.
Built with a Guardrails First philosophy, the assistant ensures high-confidence responses and distinguishes critical policies (e.g., HR rules) from general financial data.

🔑 Key Features

1. 🎯 Advanced Intent Detection

- Hybrid Classifier using valhalla/distilbart-mnli-12-1 for zero-shot classification.
- Supported intents:
- ask_finance: Financial queries (e.g., revenue, growth, strategy).
- ask_hr: HR policies, headcount, benefits.
- action_ticket: IT support requests.
- action_access: Application access requests.
- action_schedule: Meeting management.
- Smart Escalation (Rule 0): Urgent or negative queries with low confidence are escalated to human fallback.

2. 🧠 Context-Aware Memory

- Topic Switch Detection: Prevents context bleed across unrelated queries.
- Entity Scoping:
- Global entities (e.g., Employee ID, Department) persist.
- Local entities (e.g., Date, Topic) reset on topic change.

3. 📚 Enterprise RAG (Retrieval-Augmented Generation)

- Document Ingestion: FAISS + SentenceTransformers (all-MiniLM-L6-v2) index the Annual Report.
- Entity-Aware Retrieval: Prioritizes chunks with HR-relevant keywords.
- Ambiguity Detection: Flags mismatches (e.g., financial data returned for policy queries).

4. ⚙️ Action Management

- Gradio-Based UI: Interactive dashboard with real-time feedback and confirmation cards.
- Standardized JSON Output: All actions follow a strict schema for easy integration with Jira, Outlook, IAM, etc.

🧱 Technical Architecture
Core Modules
| | |
| gradio_app.py | |
| main_assistant.py | |
| intent_detector.py | |
| ner_extractor.py | |
| query_assistant.py | |
| agent_policy.py | |
| ui_formatter.py | |
| sentiment_analyzer.py | |

Data Assets

- faq_index.faiss: Vector store for Annual Report chunks.
- chunks_mapping.json: Metadata for retrieved vectors.

🚀 Getting Started

1. Environment Setup
   Ensure Python 3.10+ is installed, then install dependencies:
   pip install -r requirements.txt

2. Launch the Assistant
   python gradio_app.py

3. 📄 Beautiful HTML Documentation
   The project includes a custom-built, modern documentation page served directly via FastAPI. It covers features, tech stack, and architecture in detail.
   - **Access URL:** `http://localhost:8000/documentation` (or simply the root `/`)

4. Example Usage

- Ask a question:
  "What is the revenue growth for FY25?"
- Perform an action:
  "Schedule a meeting with the Finance team for tomorrow."
- Report an issue:
  "My laptop is extremely slow (urgent)."

Demo video link- https://drive.google.com/file/d/1XdwsUorYmzm68y7RskkhRKpUF5pRQhIU/view?usp=sharing

## 🔮 Future Roadmap & Improvements

### Improvements by Feature

#### 1. 🎯 Advanced Intent Detection

- **Multi-turn intent refinement**: Track evolving user intent across turns (e.g., a finance query that shifts into HR implications).
- **Confidence calibration**: Use ensemble scoring (combine zero-shot + keyword + historical patterns) to reduce false positives.
- **Custom intent expansion**: Add domain-specific intents (e.g., compliance, procurement, security).
- **Explainability layer**: Provide a short rationale for detected intent to build user trust.

#### 2. 🧠 Context-Aware Memory

- **Hierarchical memory**: Distinguish between session memory (short-term) and persistent memory (long-term).
- **Conflict resolution**: If global and local entities clash, prompt the user for clarification.
- **Sentiment-aware memory**: Track tone/emotion to adapt responses (e.g., urgency, frustration).
- **Privacy guardrails**: Allow users to view, edit, or delete stored entities for transparency.

#### 3. 📚 Enterprise RAG

- **Multi-source retrieval**: Expand beyond Annual Report to include policy docs, FAQs, and IT manuals.
- **Dynamic weighting**: Adjust retrieval scoring based on detected intent (finance vs HR vs IT).
- **Semantic clustering**: Group related chunks to provide holistic answers instead of isolated snippets.
- **Feedback loop**: Let users rate retrieved answers to fine-tune FAISS embeddings.

#### 4. ⚙️ Action Management

- **Adaptive UI**: Personalize dashboard views (e.g., HR queries show benefits cards, IT queries show ticket forms).
- **Action chaining**: Support multi-step workflows (e.g., schedule meeting → auto-generate invite → attach relevant docs).
- **Error recovery**: If JSON schema fails, auto-correct and retry instead of escalating immediately.
- **Analytics layer**: Track usage patterns (most common intents, escalation frequency) to optimize system design.

### 🚀 Strategic Enhancements

- **LLM Guardrails**: Add toxicity filters and compliance checks before responses.
- **Human-in-the-loop learning**: Escalated cases feed back into training data for improved automation.
- **Cross-platform integration**: Extend beyond Jira/Outlook/IAM to Slack, Teams, ServiceNow.
- **Performance optimization**: Use caching for frequently asked queries (e.g., HR policies).
