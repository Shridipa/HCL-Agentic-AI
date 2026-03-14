# Vercel Deployment Guide: HCL-Agentic-AI Frontend

This guide explains how to deploy the Next.js frontend of the HCL-Agentic-AI project to Vercel and connect it to your Render backend.

## 1. Project Configuration

The project is already configured with a `vercel.json` file in the root directory:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs"
}
```

---

## 2. Deploying to Vercel

1.  **Log in to Vercel** (vercel.com) and click **Add New** -> **Project**.
2.  **Import your GitHub repository**.
3.  **Configure Project Settings**:
    *   **Project Name**: `hcl-agentic-ai-frontend`
    *   **Framework Preset**: `Next.js`
    *   **Root Directory**: `frontend` (THIS IS CRITICAL to avoid build loops!)
4.  **Environment Variables**:
    *   Add the following variables:
        *   **`NEXT_PUBLIC_ML_BACKEND`**: `https://hcl-agentic-ai.onrender.com`
        *   **`ML_MODEL_ENDPOINT`**: `https://hcl-agentic-ai.onrender.com/api/chat`
5.  **Deploy**: Click **Deploy**.

---

## 3. Important Notes

- **CORS**: Ensure your Render backend allows requests from your Vercel domain. The `api_server.py` is currently configured to allow all origins (`allow_origins=["*"]`), which should work fine for testing.
- **Vercel Settings Overrides**: Ensure that the "Build Command" and "Install Command" in your Vercel Project Settings are **NOT** overridden. They should be set to "System Default" (unchecked). If you previously typed `cd frontend && npm install` in the Vercel UI, please clear it.

---

## Troubleshooting

If the build fails on Vercel:
- Ensure you are using the correct Node.js version (configured in Vercel settings, usually 18 or 20).
- Check the Vercel build logs for any missing dependency errors.
