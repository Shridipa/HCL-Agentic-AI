# Render Deployment Guide: HCL-Agentic-AI

This guide explains how to deploy the reorganized HCL-Agentic-AI project to Render.

## Project Structure
```
HCL-Agentic-AI/
├── backend/          # Python Fast API / Gradio backend
├── frontend/         # Next.js frontend
├── docker-compose.yml
├── package.json
└── vercel.json
```

---

## 1. Deploying the Backend (Web Service)

1.  **Log in to Render** and click **New +** -> **Web Service**.
2.  **Connect your GitHub repository**.
3.  **Configure the service**:
    *   **Name**: `hcl-agentic-ai-backend` (or any name you prefer)
    *   **Root Directory**: `backend` (This is crucial!)
    *   **Language**: `Docker`
4.  **Environment Variables**:
    *   Click the **Environment** tab.
    *   Add all keys from your `.env` file (e.g., `GROQ_API_KEY`, etc.).
5.  **Deploy**: Render will automatically build the image using `backend/Dockerfile`.

> [!TIP]
> Since we set the Root Directory to `backend`, Render will build the Docker container using only the contents of that folder.

---

## 2. Deploying the Frontend (Static Site or Web Service)

If you are deploying a Next.js app as a **Static Site** (for SSG):
1.  Click **New +** -> **Static Site**.
2.  **Root Directory**: `frontend`
3.  **Build Command**: `npm run build`
4.  **Publish Directory**: `frontend/.next` (or `out` if using `output: 'export'`)

If you want a **Web Service** (for SSR):
1.  Click **New +** -> **Web Service**.
2.  **Root Directory**: `frontend`
3.  **Build Command**: `npm install && npm run build`
4.  **Start Command**: `npm run start`

---

## 3. Connecting Frontend and Backend

Once the backend is deployed, you will get a Render URL (e.g., `https://hcl-agentic-ai-backend.onrender.com`).
1.  Go to the **Frontend** environment variables.
2.  Set `NEXT_PUBLIC_API_URL` to your backend's Render URL.

---

## Local Verification

To test the new structure locally using Docker:
```bash
docker compose up --build
```
This will start both services using the updated paths in `docker-compose.yml`.
