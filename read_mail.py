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
    # Simulated AI summary (since no ollama in sandbox)
    lines = text.strip().split("\n")

    summary = []
    for line in lines:
        if "Subject:" in line:
            summary.append(line.strip())

    return "Summary of emails:\n" + "\n".join(summary)


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
    print("\n📨 Using sample email data (sandbox mode)\n")

    email_text = """
    From: Google
    Subject: Security alert

    From: ChatGPT
    Subject: New features available

    From: Team
    Subject: Project update
    """

    print(email_text)

    print("\n🧠 AI Summary:\n")
    summary = summarize_with_llama(email_text)
    print(summary)

    save_summary(summary)


# ==============================
# 🚀 ENTRY POINT
# ==============================
if __name__ == "__main__":
    read_latest_emails()