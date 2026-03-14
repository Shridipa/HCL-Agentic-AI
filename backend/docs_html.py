
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCLTech Agentic AI | Complete Project Documentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #020617;
            --grid: rgba(30, 41, 59, 0.3);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --primary: #38bdf8;
            --secondary: #818cf8;
            
            /* Pill Colors */
            --pill-blue: #0ea5e9;
            --pill-cyan: #22d3ee;
            --pill-green: #10b981;
            --pill-amber: #f59e0b;
            --pill-purple: #a855f7;
            --pill-rose: #f43f5e;
            
            --card-bg: rgba(30, 41, 59, 0.35);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid) 1px, transparent 1px);
            background-size: 40px 40px;
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
            padding-bottom: 200px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 2.5rem;
        }

        .header-meta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-dim);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .header-meta::before {
            content: '';
            width: 40px;
            height: 1px;
            background: var(--text-dim);
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: clamp(3.5rem, 9vw, 6rem);
            font-weight: 800;
            line-height: 1;
            margin-bottom: 2.5rem;
            background: linear-gradient(to bottom right, #fff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .description {
            font-size: 1.35rem;
            color: var(--text-dim);
            max-width: 900px;
            margin-bottom: 4.5rem;
            line-height: 1.7;
        }

        h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 3rem;
            margin-bottom: 3rem;
            color: var(--text-main);
            letter-spacing: -1px;
        }

        .content-block {
            margin-bottom: 10rem;
        }

        .section-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-dim);
            text-transform: uppercase;
            margin-bottom: 2.5rem;
            display: block;
            opacity: 0.7;
        }

        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 6rem;
        }

        .pill {
            padding: 0.5rem 1.5rem;
            border-radius: 9999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 600;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--grid);
            backdrop-filter: blur(8px);
        }

        .pill.blue { border-color: var(--pill-blue); color: var(--pill-blue); }
        .pill.cyan { border-color: var(--pill-cyan); color: var(--pill-cyan); }
        .pill.green { border-color: var(--pill-green); color: var(--pill-green); }
        .pill.amber { border-color: var(--pill-amber); color: var(--pill-amber); }
        .pill.purple { border-color: var(--pill-purple); color: var(--pill-purple); }
        .pill.rose { border-color: var(--pill-rose); color: var(--pill-rose); }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
        }

        .feature-card {
            background: var(--card-bg);
            border: 1px solid var(--grid);
            border-radius: 20px;
            padding: 2.5rem;
            transition: 0.3s;
            position: relative;
            overflow: hidden;
        }

        .feature-card:hover { 
            border-color: var(--primary); 
            background: rgba(30, 41, 59, 0.5);
            transform: translateY(-5px); 
        }

        .feature-card h4 { 
            font-family: 'Outfit', sans-serif; 
            font-size: 1.5rem; 
            margin-bottom: 1rem; 
            color: var(--text-main); 
        }
        
        .feature-card p { 
            font-size: 1rem; 
            color: var(--text-dim); 
            line-height: 1.7;
        }

        .feature-card .tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--primary);
            text-transform: uppercase;
            margin-top: 1.5rem;
            display: block;
            font-weight: 700;
        }

        .pipeline-step {
            display: flex;
            gap: 2rem;
            padding: 3rem;
            background: var(--card-bg);
            border: 1px solid var(--grid);
            border-radius: 24px;
            margin-bottom: 2rem;
            transition: 0.3s;
        }

        .pipeline-step:hover {
            border-color: var(--primary);
            background: rgba(30, 41, 59, 0.5);
        }

        .step-icon {
            width: 65px; height: 65px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--grid);
            border-radius: 16px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.8rem; flex-shrink: 0;
        }

        .step-content h4 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            color: var(--text-main);
            margin-bottom: 0.75rem;
        }

        .step-content p {
            font-size: 1.1rem;
            color: var(--text-dim);
            line-height: 1.75;
        }

        .step-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            background: rgba(56, 189, 248, 0.1);
            color: var(--primary);
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
        }

        .use-case-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .use-case-item {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--grid);
            padding: 2.5rem;
            border-radius: 20px;
            transition: 0.3s;
        }

        .use-case-item:hover { border-color: var(--pill-green); transform: scale(1.02); }

        .use-case-icon { font-size: 2.5rem; margin-bottom: 1.5rem; display: block; }
        .use-case-text h4 { color: var(--text-main); font-size: 1.3rem; margin-bottom: 0.75rem; }
        .use-case-text p { color: var(--text-dim); font-size: 1rem; line-height: 1.6; }

        .setup-guide {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--grid);
            padding: 4rem;
            border-radius: 28px;
            font-family: 'JetBrains Mono', monospace;
        }

        .code-block {
            background: #000;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #10b981;
            font-size: 0.95rem;
            border: 1px solid #1e293b;
            overflow-x: auto;
            line-height: 1.6;
        }

        @media (max-width: 968px) {
            .setup-guide { padding: 2rem; }
            .pipeline-step { flex-direction: column; padding: 2.5rem; }
        }
    </style>
</head>
<body>

    <div class="container">
        
        <div class="header-meta">HCLTech Complete Project Documentation</div>

        <h1>Agentic AI<br>Deep-Dive</h1>

        <p class="description">
            A comprehensive overview of the design philosophy, modular NLP architecture, 
            and operational scaling logic of the HCLTech Enterprise Agent. This system 
            is a "Guardrails-First" implementation designed for precision data work.
        </p>

        <div class="tech-stack">
            <div class="pill blue">FastAPI</div>
            <div class="pill cyan">Next.js 15</div>
            <div class="pill green">FAISS</div>
            <div class="pill amber">DistilBART MNLI</div>
            <div class="pill purple">Groq LLAMA-3</div>
            <div class="pill rose">Transformers</div>
        </div>

        <hr style="opacity: 0.3; margin-bottom: 8rem;">

        <!-- 01: MISSION -->
        <div class="content-block">
            <span class="section-label">// 1. PROJECT MISSION & GOAL</span>
            <h2>Bridging Dialogue & Action</h2>
            <p class="body-text">
                The objective was to create a production-ready AI assistant that doesn't just "chat," but "acts." 
                By combining Retrieval-Augmented Generation (RAG) with a strict Policy Layer, we built a system 
                capable of navigating complex financial reports while automating service workflows like IT ticketing 
                and meeting management — all without risking hallucinations.
            </p>
        </div>

        <!-- 02: THE PIPELINE -->
        <div class="content-block">
            <span class="section-label">// 2. THE 5-STEP PIPELINE — ARCHITECTURAL DETAIL</span>
            <h2>The Intelligence Flow</h2>
            <p class="body-text" style="max-width: 850px;">
                Each user request passes through a strictly isolated process. This ensures that every fact is 
                mapped to an intent and verified before synthesis.
            </p>

            <div class="pipeline-step">
                <div class="step-icon">🔍</div>
                <div class="step-content">
                    <span class="step-badge">STAGE 01 — INTENT DETECTION</span>
                    <h4>Semantic Zero-Shot Routing</h4>
                    <p>We use <b>DistilBART-MNLI</b> for zero-shot classification. This removes the need for 
                    pre-trained labeled data, allowing the system to map queries to <i>Finance, HR, or IT</i> intents 
                    by understanding the semantic goal of the sentence.</p>
                </div>
            </div>

            <div class="pipeline-step">
                <div class="step-icon">🏷️</div>
                <div class="step-content">
                    <span class="step-badge">STAGE 02 — ENTITY EXTRACTION</span>
                    <h4>Automatic NER & Scoping</h4>
                    <p>Extracting dynamic variables like "Fiscal Year", "Priority", or "Department". These are stored 
                    in a session memory, allowing the AI to maintain context across multi-turn conversations.</p>
                </div>
            </div>

            <div class="pipeline-step">
                <div class="step-icon">📚</div>
                <div class="step-content">
                    <span class="step-badge">STAGE 03 — RAG RETRIEVAL</span>
                    <h4>Vector Search via FAISS</h4>
                    <p>The 100+ page Annual Report is split into 500-token chunks and vectorized. <b>FAISS</b> 
                    performs sub-millisecond similarity search to find the exact paragraph that answers the user's specific query.</p>
                </div>
            </div>

            <div class="pipeline-step">
                <div class="step-icon">🛡️</div>
                <div class="step-content">
                    <span class="step-badge">STAGE 04 — POLICY GUARD</span>
                    <h4>Validation Enforcer</h4>
                    <p>The "Guardrails-First" core. This module audits the retrieved facts against the detected intent. 
                    If the data doesn't match the goal, the enforcer flags it to prevent factual errors.</p>
                </div>
            </div>

            <div class="pipeline-step">
                <div class="step-icon">⌨️</div>
                <div class="step-content">
                    <span class="step-badge">STAGE 05 — DATA SYNTHESIS</span>
                    <h4>High-Performance Generation (Groq)</h4>
                    <p>Final response generation powered by <b>Groq (LLAMA-3 70B)</b>. This provides near-instant, professional synthesis with high factual accuracy, strictly grounded in the verified source context.</p>
                </div>
            </div>
        </div>

        <!-- 03: THE WHY -->
        <div class="content-block">
            <span class="section-label">// 3. TECHNICAL DECISIONS — THE "WHY"</span>
            <h2>Why we chose this Tech</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h4>Zero-Shot NLP</h4>
                    <p>Using BART-MNLI ensures we can add new corporate intents (like procurement or legal) in seconds, not days, without any retraining.</p>
                    <span class="tag">SCALABILITY</span>
                </div>
                <div class="feature-card">
                    <h4>Vector Retrieval</h4>
                    <p>FAISS + all-MiniLM-L6-v2 ensures semantic precision. It finds context even when the user uses different vocabulary than the PDF.</p>
                    <span class="tag">PRECISION</span>
                </div>
                <div class="feature-card">
                    <h4>FastAPI Backend</h4>
                    <p>Chosen for its high-speed asynchronicity, enabling multiple heavy AI requests to process without blocking the UI.</p>
                    <span class="tag">PERFORMANCE</span>
                </div>
                <div class="feature-card">
                    <h4>Context Memory</h4>
                    <p>Custom entities scoping prevents "context-leak," keeping HR and Finance data strictly separate during the session.</p>
                    <span class="tag">UX RELIABILITY</span>
                </div>
            </div>
        </div>

        <!-- 04: CAPABILITIES -->
        <div class="content-block">
            <span class="section-label">// 4. CORE CAPABILITIES</span>
            <h2>What the system can do</h2>
            <div class="use-case-list">
                <div class="use-case-item">
                    <span class="use-case-icon">📈</span>
                    <div class="use-case-text">
                        <h4>Financial Intelligence</h4>
                        <p>Analyze revenue, EBIDTA, and growth strategies from 100+ pages of fiscal documentation with instant citations.</p>
                    </div>
                </div>
                <div class="use-case-item">
                    <span class="use-case-icon">🎫</span>
                    <div class="use-case-text">
                        <h4>IT Service Desk</h4>
                        <p>Automatically detect issue priorities and departments to raise structured IT tickets via standardized JSON.</p>
                    </div>
                </div>
                <div class="use-case-item">
                    <span class="use-case-icon">📅</span>
                    <div class="use-case-text">
                        <h4>Agentic Scheduling</h4>
                        <p>Coordinate sync-ups and meetings by extracting dates and participants for calendar integration logic.</p>
                    </div>
                </div>
                <div class="use-case-item">
                    <span class="use-case-icon">🔐</span>
                    <div class="use-case-text">
                        <h4>Secure Access Portal</h4>
                        <p>Generate identity-scoped access requests for corporate system integrations with human-in-the-loop validation.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 05: SETUP GUIDE -->
        <div class="content-block">
            <span class="section-label">// 5. SETUP GUIDE — HOW TO OPEN & RUN</span>
            <h2>Running the Environment</h2>
            <div class="setup-guide">
                <h4 style="color: var(--primary); font-size: 1.25rem; margin-bottom: 1.5rem;">[1] Start the API Engine (FastAPI)</h4>
                <div class="code-block">
                    pip install -r requirements.txt<br>
                    python api_server.py
                </div>

                <h4 style="color: var(--secondary); font-size: 1.25rem; margin: 3rem 0 1.5rem 0;">[2] Start the Dashboard (Next.js)</h4>
                <div class="code-block">
                    cd frontend<br>
                    npm install<br>
                    npm run dev
                </div>

                <h4 style="color: #fff; font-size: 1.25rem; margin: 3rem 0 1.5rem 0;">[3] Access Endpoints</h4>
                <ul class="arch-list" style="margin-top: 1rem;">
                    <li><b>Main Dashboard:</b> Your Vercel Deployment URL</li>
                    <li><b>Technical Docs:</b> Your Render URL + /documentation</li>
                    <li><b>API Swagger UI:</b> Your Render URL + /docs</li>
                </ul>
            </div>
        </div>

        <p style="text-align: center; color: var(--text-dim); opacity: 0.5; font-size: 0.85rem; margin-top: 5rem;">
            HCLTech Project Documentation • Final Balanced Revision • 2026
        </p>

    </div>

</body>
</html>
"""
