# Google Calendar & Gmail Setup Guide

This guide configures the HCLTech AI's meeting notification system.
After completing these steps, when you schedule a meeting via chat, all participants will automatically receive **Google Calendar invites** and **professional HTML confirmation emails**.

---

## Step 1: Create a Gmail App Password (for sending emails)

> **You need 2-Step Verification enabled on your Google account first.**

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** → **2-Step Verification** → scroll down to **App passwords**
3. Click **Create app password**
4. Give it a name like `HCLTech AI` and click **Create**
5. Copy the 16-character password shown (e.g. `abcd efgh ijkl mnop`)
6. Open `.env` and set:
   ```
   ORGANIZER_EMAIL=your-gmail@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   ```

---

## Step 2: Enable Google Calendar API (for calendar invites)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g. `HCLTech-AI`)
3. Go to **APIs & Services** → **Enable APIs** → search for **Google Calendar API** → Enable it
4. Go to **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
5. Choose **Desktop application**, give it a name, click **Create**
6. Click **Download JSON** — save the file as `credentials.json` in the project root:
   ```
   c:\NLP_Challenge\HCL-Agentic-AI\credentials.json
   ```
7. Go to **OAuth consent screen** → add your Gmail address as a **Test user**

---

## Step 3: Run the First-Time OAuth Authorization

> **Run this once** to generate the `token.json` file (no need to repeat).

```powershell
# Activate your virtual environment first
.venv\Scripts\activate

# Run the test script
python -c "from calendar_email_service import _get_calendar_service; _get_calendar_service(); print('Auth successful!')"
```

A browser window will open. Log in with your Gmail account and click **Allow**.  
You'll see `Auth successful!` — a `token.json` file will be created automatically.

---

## Step 4: Update `.env`

```bash
GROQ_API_KEY=your_groq_key

# Your Gmail (must match the OAuth account)
ORGANIZER_EMAIL=your-gmail@gmail.com

# 16-char App Password from Step 1 (no spaces)
GMAIL_APP_PASSWORD=abcdefghijklmnop

# Leave as "primary" for your default calendar
GOOGLE_CALENDAR_ID=primary
```

---

## Step 5: Install Dependencies

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 6: Test It

Start the Python backend:
```powershell
python api_server.py
```

Then open the Next.js frontend and log in with your email address included.  
Type in the chat:
```
Schedule a meeting with alice@example.com about Q1 Strategy on 20th March 2026 at 3 PM
```

You will see a **green banner** confirming the Google Calendar invite and email were sent. 🎉

---

## How It Works (Flow Summary)

```
User types meeting request in chat
      ↓
NER extractor detects emails (alice@example.com), date, time, topic
      ↓
AI returns action_data { action: "schedule_meeting", participant_emails: [...], ... }
      ↓
Dashboard auto-calls Python backend: POST /api/schedule
      ↓
calendar_email_service.py:
  1. Creates Google Calendar event → Google sends invites to all attendees
  2. Sends HTML confirmation email via Gmail SMTP
      ↓
Green notification banner appears in dashboard ✅
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `credentials.json not found` | Download from Google Cloud Console (Step 2) |
| `Gmail auth failed` | Check App Password in `.env` (Step 1) |
| `Token expired` | Delete `token.json` and rerun auth (Step 3) |
| `Backend offline` | Start `python api_server.py` on port 8000 |
