# Here, we Implement the Logic for Sending Emails using the Gmail API
# Email Response layer

from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
from gmail_auth import authenticate_gmail

def send_email_gmail_api(to, subject, message_text):
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials = creds)

    message = MIMEText(message_text, "plain", "utf-8")
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    sent = service.users().messages().send(userId = "me", body = body).execute()
    return f"Email sent. ID: {sent['id']}"

# This approach gives our Agent a secure and reliable way to send Responses back to Users