
from calendar_email_service import _build_email_html

topic = "Test Meeting"
date_str = "20th March 2026"
time_str = "10:00 AM"
location = "Virtual"
participant_emails = ["dhar.shridipa@gmail.com"]
organizer_email = "dharshridipa111@gmail.com (Associate)"
meet_link = "https://meet.google.com/abc-defg-hij"

html = _build_email_html(topic, date_str, time_str, location, participant_emails, organizer_email, meet_link)

with open("/tmp/test_email.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML generated and saved to /tmp/test_email.html")
print(f"Length of HTML: {len(html)}")
