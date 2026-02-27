
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCLTech Agentic AI | Project Documentation</title>
    <meta name="description" content="Enterprise-grade AI assistant by HCLTech — Intent Detection, RAG, Smart Memory, and Action Management powered by FastAPI.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.35);
            --secondary: #a855f7;
            --bg: #0f172a;
            --bg2: #1e293b;
            --card-bg: rgba(30, 41, 59, 0.65);
            --border: rgba(255, 255, 255, 0.08);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent: #22d3ee;
            --green: #34d399;
            --orange: #fb923c;
            --red: #f87171;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html { scroll-behavior: smooth; }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            line-height: 1.7;
            overflow-x: hidden;
        }

        h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; font-weight: 700; }

        code {
            font-family: 'JetBrains Mono', monospace;
            background: rgba(99, 102, 241, 0.15);
            padding: 0.15em 0.45em;
            border-radius: 6px;
            font-size: 0.85em;
            color: var(--accent);
        }

        a { color: var(--primary); text-decoration: none; transition: color 0.2s; }
        a:hover { color: var(--accent); }

        .container { max-width: 1140px; margin: 0 auto; padding: 0 2rem; }

        /* ─── Navigation ─── */
        .nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 100;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
            padding: 0.75rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .nav-brand {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.15rem;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links { display: flex; gap: 1.5rem; align-items: center; }
        .nav-links a {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            transition: 0.2s;
        }
        .nav-links a:hover { color: var(--text-primary); }

        .nav-btn {
            background: var(--primary);
            color: #fff !important;
            padding: 0.45rem 1.1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            box-shadow: 0 2px 10px var(--primary-glow);
            transition: 0.3s;
        }
        .nav-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 18px var(--primary-glow); }

        /* ─── Hero ─── */
        .hero {
            min-height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            padding-top: 4rem;
            background:
                radial-gradient(ellipse at 30% 50%, rgba(99,102,241,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 30%, rgba(168,85,247,0.1) 0%, transparent 50%);
        }

        .hero-badge {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: var(--primary);
            padding: 0.4rem 1.2rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            animation: fadeIn 0.8s ease-out;
        }

        .hero-badge .dot {
            width: 6px; height: 6px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .hero h1 {
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 800;
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, #fff 0%, var(--primary) 50%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeInDown 1s ease-out;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            max-width: 640px;
            margin-bottom: 2.5rem;
            animation: fadeInUp 1s ease-out 0.15s backwards;
        }

        .hero-actions {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
            animation: fadeInUp 1s ease-out 0.3s backwards;
        }

        .btn {
            padding: 0.85rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: #fff;
            box-shadow: 0 4px 20px var(--primary-glow);
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 30px var(--primary-glow); color: #fff; }

        .btn-outline {
            border: 1px solid var(--border);
            color: var(--text-primary);
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(4px);
        }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); }

        /* ─── Sections ─── */
        .section { padding: 6rem 0; }
        .section-title {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        .section-subtitle {
            text-align: center;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 3.5rem;
            font-size: 1.05rem;
        }

        /* ─── Cards Grid ─── */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 1.5rem; }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.35s ease;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            opacity: 0;
            transition: opacity 0.35s;
        }
        .card:hover { transform: translateY(-4px); border-color: rgba(99,102,241,0.3); }
        .card:hover::before { opacity: 1; }

        .card-icon { font-size: 2rem; margin-bottom: 1rem; }
        .card h3 { font-size: 1.3rem; margin-bottom: 0.75rem; color: var(--text-primary); }
        .card p { color: var(--text-secondary); font-size: 0.92rem; line-height: 1.65; }

        /* ─── Plus Points ─── */
        .plus-card {
            background: rgba(255,255,255,0.02);
            padding: 2.5rem 3rem;
            border-radius: 24px;
            border: 1px solid var(--border);
        }
        .points-list { list-style: none; }
        .points-list li {
            position: relative;
            padding-left: 2.2rem;
            margin-bottom: 1.75rem;
            font-size: 1.05rem;
        }
        .points-list li::before {
            content: '◆';
            position: absolute;
            left: 0; top: 2px;
            color: var(--primary);
            font-size: 0.75rem;
        }
        .points-list li strong { display: block; margin-bottom: 0.15rem; }
        .points-list li span {
            display: block;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        /* ─── Tech Stack ─── */
        .tech-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            justify-content: center;
        }
        .tech-pill {
            background: rgba(255,255,255,0.04);
            padding: 0.6rem 1.4rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            font-weight: 500;
            font-size: 0.9rem;
            transition: 0.3s;
        }
        .tech-pill:hover { border-color: var(--accent); color: var(--accent); background: rgba(34,211,238,0.05); }

        .model-box {
            background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.08));
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 2rem;
            max-width: 650px;
            margin-inline: auto;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1.5rem;
            text-align: center;
        }
        .model-box div p:first-child { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-secondary); margin-bottom: 0.3rem; }
        .model-box div p:last-child { font-weight: 600; color: var(--accent); font-size: 0.9rem; }

        /* ─── Architecture ─── */
        .arch-container {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 24px;
            padding: 3rem;
            border: 1px solid var(--border);
        }

        .pipeline {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 2.5rem;
        }
        .pipe-node {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.85rem;
            white-space: nowrap;
        }
        .pipe-node.active { border-color: var(--primary); box-shadow: 0 0 12px var(--primary-glow); }
        .pipe-arrow { color: var(--text-secondary); font-size: 1rem; }

        .arch-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
        }
        .arch-box {
            background: rgba(0,0,0,0.25);
            padding: 1.5rem;
            border-radius: 14px;
            border: 1px solid var(--border);
        }
        .arch-box h4 { margin-bottom: 0.75rem; font-size: 1rem; }
        .arch-box ul { padding-left: 1rem; color: var(--text-secondary); font-size: 0.88rem; }
        .arch-box li { margin-bottom: 0.4rem; }

        /* ─── API Docs Banner ─── */
        .api-banner {
            background: linear-gradient(135deg, var(--bg2) 0%, rgba(99,102,241,0.1) 100%);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 3rem;
            text-align: center;
        }
        .api-banner h2 { margin-bottom: 1rem; }
        .api-banner p { color: var(--text-secondary); margin-bottom: 2rem; max-width: 500px; margin-inline: auto; }

        .doc-links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .doc-link {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 1.25rem 2rem;
            border-radius: 14px;
            text-decoration: none;
            color: var(--text-primary);
            font-weight: 600;
            transition: 0.3s;
            min-width: 180px;
        }
        .doc-link:hover { border-color: var(--primary); transform: translateY(-2px); color: var(--primary); }
        .doc-link small { display: block; color: var(--text-secondary); font-weight: 400; margin-top: 0.25rem; font-size: 0.8rem; }

        /* ─── Footer ─── */
        footer {
            padding: 3rem 0;
            text-align: center;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        /* ─── Animations ─── */
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

        /* ─── Responsive ─── */
        @media (max-width: 768px) {
            .arch-grid, .model-box { grid-template-columns: 1fr; }
            .nav-links a:not(.nav-btn) { display: none; }
            .pipeline { gap: 0.25rem; }
            .pipe-node { font-size: 0.75rem; padding: 0.5rem 0.8rem; }
        }
    </style>
</head>
<body>

    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-brand">HCLTech Agentic AI</div>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#architecture">Architecture</a>
            <a href="#tech-stack">Tech Stack</a>
            <a href="#api-docs">API</a>
            <a href="/docs" class="nav-btn">Swagger UI →</a>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="hero-badge"><span class="dot"></span> Enterprise Ready · AI Powered · FastAPI</div>
        <h1>HCLTech Agentic AI</h1>
        <p>A modular, high-confidence enterprise assistant built with FastAPI — navigating complex corporate intents with precision and guardrails.</p>
        <div class="hero-actions">
            <a href="#features" class="btn btn-primary">Explore Features</a>
            <a href="/docs" class="btn btn-outline">📄 Swagger UI</a>
            <a href="/redoc" class="btn btn-outline">📘 ReDoc</a>
        </div>
    </section>

    <div class="container">

        <!-- Core Modules -->
        <section id="features" class="section">
            <h2 class="section-title">Core Modules</h2>
            <p class="section-subtitle">Each module is independently testable and connected via the FastAPI pipeline orchestrator.</p>
            <div class="grid">
                <div class="card">
                    <div class="card-icon">🎯</div>
                    <h3>Intent Detection</h3>
                    <p>Hybrid Zero-Shot classifier using <code>DistilBART-MNLI</code>. Supports finance, HR, IT tickets, access requests, and meeting scheduling intents.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🧠</div>
                    <h3>Smart Memory</h3>
                    <p>Topic-aware entity scoping with global vs local entity management. Detects topic switches to prevent context bleed across unrelated queries.</p>
                </div>
                <div class="card">
                    <div class="card-icon">📚</div>
                    <h3>RAG Engine</h3>
                    <p>Powered by <code>FAISS</code> + <code>all-MiniLM-L6-v2</code> embeddings. Entity-aware retrieval with dynamic weighting based on detected intent.</p>
                </div>
                <div class="card">
                    <div class="card-icon">⚙️</div>
                    <h3>Action Agent</h3>
                    <p>Generates standardized JSON payloads for downstream integrations — Jira tickets, Outlook scheduling, IAM access requests.</p>
                </div>
                <div class="card">
                    <div class="card-icon">📝</div>
                    <h3>Response Generation</h3>
                    <p>Leverages <code>Flan-T5 Base</code> for synthesizing professional executive briefings with structured formatting and citations.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🛡️</div>
                    <h3>Guardrails & Citations</h3>
                    <p>Features ambiguity detection, confidence thresholds, citation enforcement, and automatic escalation for critical/negative queries.</p>
                </div>
            </div>
        </section>

        <!-- Plus Points -->
        <section class="section">
            <h2 class="section-title">Why This Project Stands Out</h2>
            <p class="section-subtitle">Key differentiators that make this more than just another chatbot.</p>
            <div class="plus-card">
                <ul class="points-list">
                    <li>
                        <strong>Guardrails-First Philosophy</strong>
                        <span>Every response is validated against confidence thresholds. HR policies and critical data are never hallucinated.</span>
                    </li>
                    <li>
                        <strong>Smart Escalation (Rule 0)</strong>
                        <span>Sentiment analysis detects frustration or urgency and triggers human fallback — preventing bad AI responses when stakes are high.</span>
                    </li>
                    <li>
                        <strong>Topic Switch Recognition</strong>
                        <span>Seamlessly handles multi-turn conversations where users jump between Finance, HR, and IT without losing global context (e.g., Employee ID).</span>
                    </li>
                    <li>
                        <strong>Standardized Action Schema</strong>
                        <span>All task-oriented intents output verified JSON conforming to strict schemas, making enterprise integration trivial.</span>
                    </li>
                    <li>
                        <strong>FastAPI-Powered Backend</strong>
                        <span>Production-ready async API with auto-generated interactive docs (Swagger UI + ReDoc), CORS support, and OpenAPI schema export.</span>
                    </li>
                </ul>
            </div>
        </section>

        <!-- Tech Stack -->
        <section id="tech-stack" class="section">
            <h2 class="section-title">Technology Stack</h2>
            <p class="section-subtitle">Built with industry-proven open-source libraries for reliability and performance.</p>
            <div class="tech-grid">
                <div class="tech-pill">🚀 FastAPI</div>
                <div class="tech-pill">🤗 Transformers</div>
                <div class="tech-pill">🔍 FAISS</div>
                <div class="tech-pill">🔥 PyTorch</div>
                <div class="tech-pill">📐 Sentence-Transformers</div>
                <div class="tech-pill">🖥️ Gradio</div>
                <div class="tech-pill">📝 NLTK</div>
                <div class="tech-pill">📊 Scikit-Learn</div>
                <div class="tech-pill">🔢 NumPy</div>
                <div class="tech-pill">🌐 Uvicorn (ASGI)</div>
                <div class="tech-pill">📦 Pydantic</div>
            </div>
            <div class="model-box">
                <div>
                    <p>Generator</p>
                    <p>flan-t5-base</p>
                </div>
                <div>
                    <p>Embeddings</p>
                    <p>all-MiniLM-L6-v2</p>
                </div>
                <div>
                    <p>Classifier</p>
                    <p>distilbart-mnli</p>
                </div>
            </div>
        </section>

        <!-- Architecture -->
        <section id="architecture" class="section">
            <h2 class="section-title">Technical Architecture</h2>
            <p class="section-subtitle">A linear pipeline orchestrated by <code>main_assistant.py</code> and served via FastAPI.</p>
            <div class="arch-container">
                <div class="pipeline">
                    <div class="pipe-node active">User Query</div>
                    <div class="pipe-arrow">→</div>
                    <div class="pipe-node">Intent Detection</div>
                    <div class="pipe-arrow">→</div>
                    <div class="pipe-node">Sentiment + NER</div>
                    <div class="pipe-arrow">→</div>
                    <div class="pipe-node active">RAG / Policy</div>
                    <div class="pipe-arrow">→</div>
                    <div class="pipe-node">Response / Action</div>
                </div>
                <div class="arch-grid">
                    <div class="arch-box">
                        <h4 style="color: var(--primary);">📂 Data Assets</h4>
                        <ul>
                            <li><code>faq_index.faiss</code> — Vector knowledge store</li>
                            <li><code>chunks_mapping.json</code> — Metadata & context mapping</li>
                            <li><code>chunks.json</code> — Raw document chunks</li>
                        </ul>
                    </div>
                    <div class="arch-box">
                        <h4 style="color: var(--secondary);">🧩 Core Modules</h4>
                        <ul>
                            <li><code>intent_detector.py</code> — Hybrid classifier</li>
                            <li><code>agent_policy.py</code> — Decision routing</li>
                            <li><code>action_generator.py</code> — JSON builder</li>
                            <li><code>citation_enforcer.py</code> — Fact verification</li>
                        </ul>
                    </div>
                    <div class="arch-box">
                        <h4 style="color: var(--accent);">🔌 API Layer (FastAPI)</h4>
                        <ul>
                            <li><code>POST /api/chat</code> — Main AI endpoint</li>
                            <li><code>GET /health</code> — Status check</li>
                            <li><code>GET /docs</code> — Swagger UI</li>
                            <li><code>GET /redoc</code> — ReDoc reference</li>
                            <li><code>GET /openapi.json</code> — Schema export</li>
                        </ul>
                    </div>
                    <div class="arch-box">
                        <h4 style="color: var(--green);">🖥️ Frontend</h4>
                        <ul>
                            <li><code>gradio_app.py</code> — Internal Gradio dashboard</li>
                            <li><code>nlp_folder/</code> — Next.js web frontend</li>
                            <li><code>/documentation</code> — This docs page</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- API Documentation Banner -->
        <section id="api-docs" class="section">
            <div class="api-banner">
                <h2>📡 Interactive API Documentation</h2>
                <p>Explore, test, and integrate with the HCLTech Agentic AI API using auto-generated interactive documentation.</p>
                <div class="doc-links">
                    <a href="/docs" class="doc-link">
                        ⚡ Swagger UI
                        <small>Interactive API playground</small>
                    </a>
                    <a href="/redoc" class="doc-link">
                        📘 ReDoc
                        <small>Clean API reference</small>
                    </a>
                    <a href="/openapi.json" class="doc-link">
                        📄 OpenAPI JSON
                        <small>Export schema for tools</small>
                    </a>
                    <a href="/health" class="doc-link">
                        💚 Health Check
                        <small>Server status</small>
                    </a>
                </div>
            </div>
        </section>

    </div>

    <footer>
        <p>Built with ❤️ for the HCLTech NLP Challenge — Powered by <strong>FastAPI</strong></p>
        <p style="margin-top: 0.4rem; opacity: 0.5;">&copy; 2025 HCLTech Agentic AI · v1.0.0</p>
    </footer>

    <script>
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(a => {
            a.addEventListener('click', e => {
                e.preventDefault();
                const target = document.querySelector(a.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        });

        // Animate cards on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.card, .arch-box, .doc-link').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    </script>
</body>
</html>
"""
