
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCLTech Agentic AI | Project Documentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.35);
            --secondary: #a855f7;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #22d3ee;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }

        h1, h2, h3 { font-family: 'Outfit', sans-serif; font-weight: 700; }
        .container { max-width: 1100px; margin: 0 auto; padding: 0 2rem; }

        /* Hero */
        .hero {
            height: 85vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: radial-gradient(circle at center, var(--primary-glow) 0%, transparent 70%);
        }

        .hero h1 {
            font-size: clamp(2.5rem, 8vw, 4.5rem);
            margin-bottom: 1.5rem;
            background: linear-gradient(to right, #fff, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            max-width: 700px;
            margin-bottom: 2rem;
        }

        .badge {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 0.5rem 1.2rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }

        /* Features */
        .section { padding: 5rem 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.5rem;
            transition: 0.3s;
        }
        .card:hover { transform: translateY(-5px); border-color: var(--primary); }
        .card h3 { color: var(--accent); margin-bottom: 1rem; }

        /* Points */
        .points-box {
            background: rgba(255,255,255,0.02);
            padding: 3rem;
            border-radius: 24px;
            border: 1px solid var(--border);
        }
        .points-list { list-style: none; }
        .points-list li {
            padding-left: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
        }
        .points-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }
        .points-list strong { display: block; }
        .points-list span { color: var(--text-secondary); font-size: 0.9rem; }

        /* Tech Stack */
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }
        .tech-item {
            background: rgba(255,255,255,0.05);
            padding: 0.7rem 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            font-weight: 500;
        }

        footer {
            padding: 4rem 0;
            text-align: center;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

    <section class="hero">
        <div class="badge">Official Project Documentation</div>
        <h1>HCLTech Agentic AI</h1>
        <p>A high-performance enterprise assistant built with FastAPI, designed for high-confidence responses and seamless action management.</p>
        <a href="#features" style="background: var(--primary); color: white; padding: 0.8rem 2.5rem; border-radius: 12px; text-decoration: none; font-weight: 600; margin-top: 1rem;">Explore Project</a>
    </section>

    <div class="container">
        
        <section id="features" class="section">
            <h2 style="text-align: center; margin-bottom: 3rem;">Core Capabilities</h2>
            <div class="grid">
                <div class="card">
                    <h3>🎯 Intent Detection</h3>
                    <p>Hybrid classifier utilizing DistilBART-MNLI for zero-shot categorization of corporate queries.</p>
                </div>
                <div class="card">
                    <h3>🧠 Smart Memory</h3>
                    <p>Maintains context while preventing cross-topic bleeding. Manages global vs local entities effectively.</p>
                </div>
                <div class="card">
                    <h3>📚 RAG Engine</h3>
                    <p>Semantic retrieval system powered by FAISS and Sentence-Transformers for highly relevant data extraction.</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 style="text-align: center; margin-bottom: 3rem;">Project Plus Points</h2>
            <div class="points-box">
                <ul class="points-list">
                    <li>
                        <strong>Guardrails First Philosophy</strong>
                        <span>Ensures high-confidence responses for critical policies and financial data.</span>
                    </li>
                    <li>
                        <strong>Smart Escalation</strong>
                        <span>Sentiment-aware logic that identifies high-urgency or negative queries for human fallback.</span>
                    </li>
                    <li>
                        <strong>Standardized Action Schema</strong>
                        <span>Generates verifiable JSON output for direct integration with enterprise systems.</span>
                    </li>
                </ul>
            </div>
        </section>

        <section class="section">
            <h2 style="text-align: center; margin-bottom: 3rem;">Technology Stack</h2>
            <div class="tech-stack">
                <div class="tech-item">FastAPI</div>
                <div class="tech-item">Transformers</div>
                <div class="tech-item">FAISS</div>
                <div class="tech-item">PyTorch</div>
                <div class="tech-item">Sentence-Transformers</div>
                <div class="tech-item">Gradio</div>
                <div class="tech-item">NLTK</div>
            </div>
        </section>

    </div>

    <footer>
        <p>Built with ❤️ for HCLTech NLP Challenge</p>
    </footer>

</body>
</html>
"""
