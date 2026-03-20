import sys
sys.path.append("./libs")

import imaplib
import email
import subprocess
from datetime import datetime


# ==============================
# 🔐 CONFIG (CHANGE THIS)
# ==============================
EMAIL = "saiyesnew@gmail.com"
PASSWORD = "sai@12345"   # ⚠️ Use Gmail App Password


# ==============================
# 🧠 LLM SUMMARY (OLLAMA)
# ==============================
def summarize_with_llama(text):
    prompt = f"Summarize these emails clearly:\n{text}"

    result = subprocess.run(
        ["ollama", "run", "llama3.3:latest"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()


# ==============================
# 💾 SAVE SUMMARY
# ==============================
def save_summary(summary):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"summary_{now}.txt"

    with open(filename, "w") as f:
        f.write(summary)

    print(f"\n💾 Summary saved to {filename}")


# ==============================
# 📧 READ EMAILS (IMAP)
# ==============================
def read_latest_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    email_text = ""

    print("\n📨 Raw Emails:\n")

    for i in mail_ids[-5:]:
        status, msg_data = mail.fetch(i, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                sender = msg["from"]
                subject = msg["subject"]

                print("From:", sender)
                print("Subject:", subject)
                print("-" * 40)

                email_text += f"From: {sender}\nSubject: {subject}\n\n"

    mail.logout()

    print("\n🧠 AI Summary:\n")
    summary = summarize_with_llama(email_text)
    print(summary)

    save_summary(summary)


# ==============================
# 🚀 ENTRY POINT
# ==============================
if __name__ == "__main__":
    read_latest_emails()