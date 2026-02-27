
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCLTech Agentic AI | Project Documentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.4);
            --secondary: #a855f7;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #22d3ee;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }

        h1, h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Hero Section */
        .hero {
            height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            background: radial-gradient(circle at center, var(--primary-glow) 0%, transparent 70%);
        }

        .hero h1 {
            font-size: 4rem;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #fff, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeInDown 1s ease-out;
        }

        .hero p {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 700px;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out 0.2s backwards;
        }

        .badge {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            display: inline-block;
            animation: fadeIn 1s ease-out;
        }

        /* Glassmorphism Section */
        .section {
            padding: 5rem 0;
        }

        .section-title {
            font-size: 2.5rem;
            margin-bottom: 3rem;
            text-align: center;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            box-shadow: 0 10px 30px -10px var(--primary-glow);
        }

        .card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }

        .card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        /* Plus Points List */
        .points-list {
            list-style: none;
        }

        .points-list li {
            position: relative;
            padding-left: 2rem;
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }

        .points-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
            font-size: 1.2rem;
        }

        .points-list span {
            display: block;
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 0.2rem;
        }

        /* Tech Stack */
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }

        .tech-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            font-weight: 500;
            transition: 0.3s;
        }

        .tech-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--accent);
            color: var(--accent);
        }

        /* Architecture Section */
        .arch-viz {
            background: rgba(15, 23, 42, 0.5);
            border-radius: 24px;
            padding: 3rem;
            border: 1px dashed var(--border);
            margin-top: 2rem;
            text-align: center;
        }

        .flows {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 800px;
            margin: 0 auto;
        }

        .node {
            background: var(--card-bg);
            border: 1px solid var(--primary);
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
        }

        .arrow {
            color: var(--text-secondary);
            font-size: 1.5rem;
        }

        /* Animations */
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

        footer {
            padding: 4rem 0;
            text-align: center;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .gradient-text {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .highlight-box {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
        }
    </style>
</head>
<body>

    <section class="hero">
        <div class="badge">Enterprise Ready · AI Powered</div>
        <h1>HCLTech Agentic AI</h1>
        <p>A modular, high-confidence enterprise assistant designed to navigate complex corporate intents with precision.</p>
        <div style="margin-top: 2rem; display: flex; gap: 1rem;">
            <a href="#features" style="text-decoration: none; background: var(--primary); color: white; padding: 0.8rem 2rem; border-radius: 12px; font-weight: 600; box-shadow: 0 4px 14px 0 var(--primary-glow);">Explore Features</a>
            <a href="/docs" style="text-decoration: none; border: 1px solid var(--border); color: var(--text-primary); padding: 0.8rem 2rem; border-radius: 12px; font-weight: 600; backdrop-filter: blur(4px);">API Reference</a>
        </div>
    </section>

    <div class="container">
        
        <section id="features" class="section">
            <h2 class="section-title">Core Modules</h2>
            <div class="grid">
                <div class="card">
                    <h3>🎯 Intent Detection</h3>
                    <p>Uses a hybrid Zero-Shot classifier (<b>DistilBART-MNLI</b>) to categorize queries into Finance, HR, IT Tickets, and more with high precision.</p>
                </div>
                <div class="card">
                    <h3>🧠 Smart Memory</h3>
                    <p>Topic-aware entity scoping. Recognizes when users switch contexts and manages global vs local entities (e.g., Employee ID stays, Topic resets).</p>
                </div>
                <div class="card">
                    <h3>📚 RAG Engine</h3>
                    <p>Powered by <b>FAISS</b> and <b>Sentence-Transformers (all-MiniLM-L6-v2)</b>. Retrieves relevant context from the HCL Annual Report with entity-aware filtering.</p>
                </div>
                <div class="card">
                    <h3>⚙️ Action Agent</h3>
                    <p>Generates standardized JSON payloads using specialized prompting, bridging natural language to enterprise systems (Jira, Outlook, IAM).</p>
                </div>
                <div class="card">
                    <h3>📝 Generation</h3>
                    <p>Leverages <b>Flan-T5 (Base/Small)</b> for synthesizing professional executive briefings based on retrieved data and context.</p>
                </div>
                <div class="card">
                    <h3>🛡️ Guardrails</h3>
                    <p>Features an <b>Ambiguity Detection</b> layer and <b>Citation Enforcement</b> to ensure every fact presented is backed by the source material.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Why This Project? <span class="gradient-text">Plus Points</span></h2>
            <div style="background: rgba(255,255,255,0.02); padding: 3rem; border-radius: 24px; border: 1px solid var(--border);">
                <ul class="points-list">
                    <li>
                        <strong>Guardrails First Philosophy</strong>
                        <span>Every response is validated against confidence thresholds to prevent hallucinations in critical areas like HR policies.</span>
                    </li>
                    <li>
                        <strong>Smart escalation (Rule 0)</strong>
                        <span>Automatically detects frustration or high-urgency queries using <b>Sentiment Analysis</b> and triggers human fallback.</span>
                    </li>
                    <li>
                        <strong>Topic Switch Recognition</strong>
                        <span>Seamlessly handles multi-turn conversations where the user jumps from Finance queries to HR requests without losing global context.</span>
                    </li>
                    <li>
                        <strong>Standardized Action Schema</strong>
                        <span>All task-oriented intents are converted into verifiable JSON, making integration with external APIs trivial.</span>
                    </li>
                    <li>
                        <strong>Optimized Performance</strong>
                        <span>Lightweight models and efficient vector search ensure high responsiveness even on standard CPU infrastructure.</span>
                    </li>
                </ul>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Technology Stack</h2>
            <div class="tech-stack">
                <div class="tech-item">FastAPI</div>
                <div class="tech-item">Transformers (HuggingFace)</div>
                <div class="tech-item">FAISS (Vector DB)</div>
                <div class="tech-item">PyTorch</div>
                <div class="tech-item">Sentence-Transformers</div>
                <div class="tech-item">Gradio (Internal UI)</div>
                <div class="tech-item">NLTK</div>
                <div class="tech-item">Scikit-Learn</div>
                <div class="tech-item">NumPy</div>
            </div>
            <div class="highlight-box" style="text-align: center; max-width: 600px; margin: 2rem auto;">
                <p><strong>Primary Model:</strong> google/flan-t5-base</p>
                <p><strong>Embeddings:</strong> sentence-transformers/all-MiniLM-L6-v2</p>
                <p><strong>Classifier:</strong> valhalla/distilbart-mnli-12-1</p>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Technical Architecture</h2>
            <div class="arch-viz">
                <div class="flows">
                    <div class="node">User Query</div>
                    <div class="arrow">→</div>
                    <div class="node" style="border-color: var(--secondary);">Agent Pipeline</div>
                    <div class="arrow">→</div>
                    <div class="node">Response / Action</div>
                </div>
                <p style="margin-top: 3rem; color: var(--text-secondary); max-width: 600px; margin-inline: auto;">
                    The system follows a modular pipeline orchestrated by <code>main_assistant.py</code>. It passes through <b>Intent Detection</b>, <b>Sentiment Analysis</b>, <b>Entity Extraction</b>, and finally <b>Agent Policy Decision</b>.
                </p>
                <div style="margin-top: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: left;">
                    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 12px;">
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Data Assets</h4>
                        <ul style="color: var(--text-secondary); font-size: 0.9rem; padding-left: 1rem;">
                            <li><code>faq_index.faiss</code> - Vector knowledge store</li>
                            <li><code>chunks_mapping.json</code> - Metadata & context mapping</li>
                        </ul>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 12px;">
                        <h4 style="color: var(--secondary); margin-bottom: 0.5rem;">Core Logic</h4>
                        <ul style="color: var(--text-secondary); font-size: 0.9rem; padding-left: 1rem;">
                            <li><code>intent_detector.py</code> - Hybrid classifier</li>
                            <li><code>agent_policy.py</code> - Decision routing logic</li>
                            <li><code>action_generator.py</code> - JSON schema builder</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <footer>
        <p>Built with ❤️ for HCLTech NLP Challenge</p>
        <p style="margin-top: 0.5rem; opacity: 0.6;">&copy; 2024 HCLTech Agentic AI. Documentation served via FastAPI.</p>
    </footer>

    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>
"""
