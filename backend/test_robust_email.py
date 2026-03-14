
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from calendar_email_service import _build_email_html, _build_email_text

# Mock data
topic = "Robust Test Meeting 📅"
date_str = "21st March 2026"
time_str = "2:00 PM"
location = "Virtual"
participant_emails = ["dhar.shridipa@gmail.com"]
organizer_email = "dharshridipa111@gmail.com"
organizer_name = "Shridipa"
meet_link = "https://meet.google.com/test-link"

text_body = _build_email_text(topic, date_str, time_str, location, participant_emails, f"{organizer_name} ({organizer_email})", meet_link)
html_body = _build_email_html(topic, date_str, time_str, location, participant_emails, f"{organizer_name} ({organizer_email})", meet_link)

print("--- Text Body ---")
print(text_body)
print("\n--- HTML Body Snippet ---")
print(html_body[:200])

# Simulate message structure
msg = MIMEMultipart("alternative")
msg["Subject"] = f"📅 Meeting Invitation: {topic}"
msg.attach(MIMEText(text_body, "plain", "utf-8"))
msg.attach(MIMEText(html_body, "html", "utf-8"))

print("\n--- Message MIME Structure ---")
for part in msg.walk():
    print(f"Content-Type: {part.get_content_type()}, Charset: {part.get_content_charset()}")

with open("/tmp/test_robust_email.eml", "w", encoding="utf-8") as f:
    f.write(msg.as_string())

print("\nSaved simulated message to /tmp/test_robust_email.eml")
