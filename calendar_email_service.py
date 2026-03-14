"""
calendar_email_service.py
--------------------------
Handles Google Calendar event creation and email notifications
when a meeting is scheduled via the HCLTech Agentic AI chatbot.

FLOW:
  1. User types meeting request in chat (includes participant emails)
  2. AI extracts entities (topic, date, time, participants, participant_emails)
  3. On confirmation, this module:
     a) Creates a Google Calendar event with all attendees → Google auto-sends invites
     b) Sends a formatted HTML confirmation email via Gmail SMTP to all participants

SETUP (one-time):
  - Place 'credentials.json' from Google Cloud Console in project root
  - Add ORGANIZER_EMAIL and GMAIL_APP_PASSWORD to .env
  - Run once interactively to generate token.json (OAuth2 flow)
"""

import os
import json
import smtplib
import datetime
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

ORGANIZER_EMAIL = os.getenv("ORGANIZER_EMAIL", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


# ─────────────────────────────────────────────
# 1. Google Calendar Integration
# ─────────────────────────────────────────────

def _get_calendar_service():
    """Returns an authenticated Google Calendar service object."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        "credentials.json not found. Please download it from Google Cloud Console "
                        "and place it in the project root. See GOOGLE_SETUP.md for instructions."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        service = build("calendar", "v3", credentials=creds)
        return service
    except ImportError:
        raise ImportError(
            "Google API libraries not installed. Run: "
            "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
        )


def _parse_datetime(date_str: str, time_str: str):
    """
    Parses natural date/time strings into ISO 8601 format.
    Returns (start_dt_str, end_dt_str) both in ISO format, 1-hour duration.
    """
    now = datetime.datetime.now()

    # Date parsing
    date_obj = None
    date_str_clean = str(date_str).strip().lower()

    if date_str_clean in ("tbd", "...", ""):
        date_obj = now.date() + datetime.timedelta(days=1)
    elif date_str_clean == "today":
        date_obj = now.date()
    elif date_str_clean == "tomorrow":
        date_obj = now.date() + datetime.timedelta(days=1)
    elif date_str_clean == "next week":
        date_obj = now.date() + datetime.timedelta(weeks=1)
    else:
        # Try various formats
        for fmt in ("%d %B %Y", "%B %d %Y", "%B %d, %Y", "%d %B", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"):
            try:
                parsed = datetime.datetime.strptime(date_str_clean.replace(",", "").title(), fmt)
                date_obj = parsed.date()
                if date_obj.year == 1900:
                    date_obj = date_obj.replace(year=now.year)
                break
            except ValueError:
                continue
        if not date_obj:
            # Handle ordinal dates like "20th March 2026"
            clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_clean, flags=re.IGNORECASE)
            for fmt in ("%d %B %Y", "%d %B", "%B %d %Y"):
                try:
                    parsed = datetime.datetime.strptime(clean.strip().title(), fmt)
                    date_obj = parsed.date()
                    if date_obj.year == 1900:
                        date_obj = date_obj.replace(year=now.year)
                    break
                except ValueError:
                    continue
        if not date_obj:
            date_obj = now.date() + datetime.timedelta(days=1)

    # Time parsing
    time_obj = datetime.time(10, 0)  # default 10:00 AM
    time_str_clean = str(time_str).strip().upper().replace("AT ", "").replace("AROUND ", "")

    for fmt in ("%I:%M %p", "%I %p", "%H:%M", "%I:%M%p", "%I%p"):
        try:
            time_obj = datetime.datetime.strptime(time_str_clean, fmt).time()
            break
        except ValueError:
            continue

    start_dt = datetime.datetime.combine(date_obj, time_obj)
    end_dt = start_dt + datetime.timedelta(hours=1)

    tz = "Asia/Kolkata"
    return start_dt.isoformat(), end_dt.isoformat(), tz


def create_google_calendar_event(
    topic: str,
    date_str: str,
    time_str: str,
    location: str,
    participant_emails: list,
    organizer_email: str
) -> dict:
    """
    Creates a Google Calendar event and sends invites to all attendees.
    Returns a result dict with success status and event link.
    """
    try:
        service = _get_calendar_service()
        start_iso, end_iso, tz = _parse_datetime(date_str, time_str)

        attendees = [{"email": email.strip()} for email in participant_emails if email.strip()]
        if organizer_email and organizer_email not in participant_emails:
            attendees.append({"email": organizer_email})

        event = {
            "summary": topic,
            "location": location if location not in ("Virtual", "TBD", "...") else "Google Meet / Virtual",
            "description": (
                f"This meeting was scheduled via HCLTech Agentic AI Assistant.\n\n"
                f"Topic: {topic}\n"
                f"Organizer: {organizer_email}"
            ),
            "start": {"dateTime": start_iso, "timeZone": tz},
            "end": {"dateTime": end_iso, "timeZone": tz},
            "attendees": attendees,
            "conferenceData": {
                "createRequest": {
                    "requestId": f"hcl-ai-{int(datetime.datetime.now().timestamp())}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}
                }
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 60},
                    {"method": "popup", "minutes": 15}
                ]
            },
            "guestsCanModifyEvent": False,
            "sendUpdates": "all"  # Google sends invite emails automatically
        }

        created_event = service.events().insert(
            calendarId=GOOGLE_CALENDAR_ID,
            body=event,
            conferenceDataVersion=1,
            sendUpdates="all"
        ).execute()

        meet_link = created_event.get("hangoutLink", "")
        event_link = created_event.get("htmlLink", "")

        return {
            "success": True,
            "event_id": created_event.get("id"),
            "event_link": event_link,
            "meet_link": meet_link,
            "message": f"Google Calendar event created. Invites sent to {len(attendees)} participant(s)."
        }

    except FileNotFoundError as e:
        return {"success": False, "error": str(e), "message": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"Calendar error: {str(e)}"}


# ─────────────────────────────────────────────
# 2. Email Notification (SMTP via Gmail)
# ─────────────────────────────────────────────

def _build_email_html(topic, date_str, time_str, location, participant_emails, organizer_email, meet_link=""):
    """Builds a polished HTML email for the meeting confirmation."""
    participants_html = "".join(
        f"<li style='margin-bottom:4px;'>📧 {email}</li>" for email in participant_emails
    )
    meet_section = ""
    if meet_link:
        meet_section = f"""
        <tr>
          <td style="padding:8px 0;">
            <span style="color:#6b7280;font-weight:600;">🔗 Google Meet:</span>
            <a href="{meet_link}" style="color:#7353ba;text-decoration:none;margin-left:8px;">{meet_link}</a>
          </td>
        </tr>"""

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Meeting Invitation</title></head>
<body style="margin:0;padding:0;background:#f0f0f0;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:30px 0;">
      <table width="580" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.1);">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#2f195f,#7353ba);padding:28px 32px;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:white;width:40px;height:40px;border-radius:8px;text-align:center;vertical-align:middle;font-size:20px;">🧠</td>
                <td style="padding-left:12px;">
                  <span style="color:white;font-weight:800;font-size:18px;">HCLTech Agentic AI</span><br>
                  <span style="color:#d8c4ff;font-size:12px;">Meeting Confirmation</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:28px 32px;">
            <h2 style="margin:0 0 6px;color:#0f1020;font-size:22px;">📅 You're Invited!</h2>
            <p style="margin:0 0 20px;color:#6b7280;font-size:14px;">
              A meeting has been scheduled for you via the HCLTech Agentic AI Assistant.
            </p>

            <div style="background:#f8f5ff;border-left:4px solid #7353ba;border-radius:8px;padding:20px;margin-bottom:24px;">
              <h3 style="margin:0 0 16px;color:#2f195f;font-size:18px;">{topic}</h3>
              <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="padding:8px 0;color:#374151;">
                    <span style="color:#6b7280;font-weight:600;">📅 Date:</span>
                    <span style="margin-left:8px;">{date_str}</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;color:#374151;">
                    <span style="color:#6b7280;font-weight:600;">⏰ Time:</span>
                    <span style="margin-left:8px;">{time_str}</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;color:#374151;">
                    <span style="color:#6b7280;font-weight:600;">📍 Location:</span>
                    <span style="margin-left:8px;">{location if location not in ('...', 'TBD') else 'Virtual / Google Meet'}</span>
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;color:#374151;">
                    <span style="color:#6b7280;font-weight:600;">👤 Organizer:</span>
                    <span style="margin-left:8px;">{organizer_email}</span>
                  </td>
                </tr>
                {meet_section}
              </table>
            </div>

            <h4 style="color:#374151;margin:0 0 8px;">Participants</h4>
            <ul style="margin:0 0 24px;padding-left:20px;color:#374151;font-size:14px;">
              {participants_html}
            </ul>

            {"<a href='" + meet_link + "' style='display:inline-block;background:linear-gradient(90deg,#7353ba,#2f195f);color:white;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;'>🎥 Join Google Meet</a>" if meet_link else ""}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f8f8f8;padding:16px 32px;text-align:center;">
            <p style="margin:0;color:#9ca3af;font-size:11px;">
              This invitation was generated automatically by HCLTech Agentic AI Assistant.<br>
              Please do not reply directly to this email.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _build_email_text(topic, date_str, time_str, location, participant_emails, organizer_email, meet_link=""):
    """Builds a plain-text fallback version of the meeting invitation."""
    participants_str = "\n".join(f"- {email}" for email in participant_emails)
    return f"""
📅 Meeting Invitation: {topic}

A meeting has been scheduled for you via the HCLTech Agentic AI Assistant.

Topic: {topic}
Date: {date_str}
Time: {time_str}
Location: {location if location not in ('...', 'TBD') else 'Virtual / Google Meet'}
Organizer: {organizer_email}

Participants:
{participants_str}

{f"Join Google Meet: {meet_link}" if meet_link else ""}

Note: This invitation was generated automatically. Please do not reply directly to this email.
""".strip()


def send_confirmation_email(
    topic: str,
    date_str: str,
    time_str: str,
    location: str,
    participant_emails: list,
    organizer_email: str,
    organizer_name: str = "Associate",
    meet_link: str = ""
) -> dict:
    """
    Sends a professional HTML meeting confirmation email to all participants.
    Uses Gmail SMTP with App Password from .env (GMAIL_APP_PASSWORD).
    """
    if not ORGANIZER_EMAIL or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "message": "ORGANIZER_EMAIL or GMAIL_APP_PASSWORD not set in .env file."
        }

    all_recipients = list(set([e.strip() for e in participant_emails if e.strip()]))
    if organizer_email and organizer_email not in all_recipients:
        all_recipients.append(organizer_email)

    if not all_recipients:
        return {"success": False, "message": "No valid recipient emails provided."}

    text_body = _build_email_text(topic, date_str, time_str, location, all_recipients, f"{organizer_name} ({organizer_email})", meet_link)
    html_body = _build_email_html(topic, date_str, time_str, location, all_recipients, f"{organizer_name} ({organizer_email})", meet_link)

    errors: list[str] = []
    sent_count: int = 0

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(ORGANIZER_EMAIL, GMAIL_APP_PASSWORD)

            for recipient in all_recipients:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"📅 Meeting Invitation: {topic}"
                msg["From"] = f"{organizer_name} (HCL AI) <{ORGANIZER_EMAIL}>"
                msg["To"] = recipient
                
                # Attach both parts - Plain text first, then HTML
                msg.attach(MIMEText(text_body, "plain", "utf-8"))
                msg.attach(MIMEText(html_body, "html", "utf-8"))

                try:
                    server.sendmail(ORGANIZER_EMAIL, recipient, msg.as_string())
                    sent_count += 1
                except Exception as e:
                    errors.append(f"{recipient}: {str(e)}")

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": "Gmail authentication failed. Check ORGANIZER_EMAIL and GMAIL_APP_PASSWORD in .env."
        }
    except Exception as e:
        return {"success": False, "message": f"SMTP error: {str(e)}"}

    if errors:
        return {
            "success": sent_count > 0,
            "message": f"Sent to {sent_count}/{len(all_recipients)} recipients. Errors: {'; '.join(errors)}"
        }

    return {
        "success": True,
        "message": f"Confirmation email sent to {sent_count} participant(s)."
    }


# ─────────────────────────────────────────────
# 3. Main Orchestrator
# ─────────────────────────────────────────────

def schedule_and_notify(action_data: dict, organizer_email: str = "", organizer_name: str = "Associate") -> dict:
    """
    Main entry point called when user confirms a schedule_meeting action.
    
    Args:
        action_data: dict from action_generator containing topic, date, time,
                     location, participants, participant_emails
        organizer_email: the logged-in user's email (from login session)
        organizer_name: the logged-in user's name
    
    Returns:
        dict with calendar_result, email_result, and combined status
    """
    org_email = organizer_email.strip() if (organizer_email and organizer_email.strip()) else ORGANIZER_EMAIL

    topic = action_data.get("topic", "Meeting")
    date_str = action_data.get("date", "TBD")
    time_str = action_data.get("time", "TBD")
    location = action_data.get("location", "Virtual")
    participant_emails = action_data.get("participant_emails", [])

    if isinstance(participant_emails, str):
        participant_emails = [e.strip() for e in participant_emails.split(",") if e.strip()]

    # Step 1: Create Google Calendar event
    calendar_result = create_google_calendar_event(
        topic=topic,
        date_str=date_str,
        time_str=time_str,
        location=location,
        participant_emails=participant_emails,
        organizer_email=org_email
    )

    meet_link = calendar_result.get("meet_link", "")

    # Step 2: Send confirmation email
    email_result = send_confirmation_email(
        topic=topic,
        date_str=date_str,
        time_str=time_str,
        location=location,
        participant_emails=participant_emails,
        organizer_email=org_email,
        organizer_name=organizer_name,
        meet_link=meet_link
    )

    all_success = calendar_result.get("success") and email_result.get("success")
    partial = calendar_result.get("success") or email_result.get("success")

    status = "success" if all_success else ("partial" if partial else "failed")

    return {
        "status": status,
        "calendar": calendar_result,
        "email": email_result,
        "meet_link": meet_link,
        "summary": (
            f"✅ Calendar invite sent & email delivered to {len(participant_emails)} participant(s)."
            if all_success else
            f"⚠️ Partial: Calendar={calendar_result.get('success')}, Email={email_result.get('success')}. "
            f"Details: {calendar_result.get('message','')} | {email_result.get('message','')}"
            if partial else
            f"❌ Failed to send notifications. {calendar_result.get('message','')} | {email_result.get('message','')}"
        )
    }
