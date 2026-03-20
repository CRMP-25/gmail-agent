import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔒 ONLY READ-ONLY ACCESS
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

import subprocess

def summarize_with_llama(text):
    prompt = f"Summarize these emails clearly:\n{text}"

    result = subprocess.run(
        ["ollama", "run", "llama3.3:latest"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()


from datetime import datetime

def save_summary(summary):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"summary_{now}.txt"

    with open(filename, "w") as f:
        f.write(summary)

    print(f"\n💾 Summary saved to {filename}")


import base64
from email.mime.text import MIMEText

def send_email(service, summary):
    message = MIMEText(summary)
    message['to'] = "saiyesnew@gmail.com"
    message['from'] = "me"
    message['subject'] = "🧠 AI Email Summary"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    print("📧 Summary email sent successfully!")

def get_gmail_service():
    creds = None

    # token.json stores login session
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid creds → login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def read_latest_emails():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No emails found.")
        return

    email_text = ""

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = msg_data['payload']['headers']

        subject = next(
            (h['value'] for h in headers if h['name'] == 'Subject'),
            "No Subject"
        )

        sender = next(
            (h['value'] for h in headers if h['name'] == 'From'),
            "Unknown"
        )

        email_text += f"From: {sender}\nSubject: {subject}\n\n"

    print("\n📨 Raw Emails:\n")
    print(email_text)

    print("\n🧠 AI Summary:\n")
    summary = summarize_with_llama(email_text)
    print(summary)

    save_summary(summary)
    # new
    service = get_gmail_service()
    send_email(service, summary)


if __name__ == "__main__":
    read_latest_emails()