#!/usr/bin/env python3
"""Send test email to alexandertianlin@gmail.com using auto-email-sender skill."""
import smtplib, ssl, os, sys, getpass
from email.mime.text import MIMEText

SENDER = "alexandertianlin@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Natural language test email (no AI markers)
BODY = """Hi there,

I'm testing the auto-email-sender skill I built. If you're reading this, it means the Gmail SMTP integration works properly.

The email content is written in plain natural language - no bullet points, no structured lists, no "I am writing to express" type of stuff. Just a straightforward message.

This is the skill that can send job application emails on my behalf, with human-written content that doesn't look AI-generated.

Cool, right?

Best"""
SUBJECT = "Test - auto-email-sender skill"

def main():
    msg = MIMEText(BODY, "plain", "utf-8")
    msg["From"] = SENDER
    msg["To"] = SENDER
    msg["Subject"] = SUBJECT

    pwd = os.environ.get("GMAIL_APP_PASSWORD")
    if not pwd:
        try:
            pwd = getpass.getpass(f"Gmail App Password for {SENDER}: ")
        except:
            pwd = None

    if not pwd:
        print("ERROR: GMAIL_APP_PASSWORD is required.")
        print("Set it as environment variable or enter it when prompted.")
        print()
        print("To get an App Password:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Search for 'App passwords'")
        print("4. Generate a 16-character password")
        print()
        print("Then run:")
        print(f"  GMAIL_APP_PASSWORD=your16charapppassword python3 {__file__}")
        sys.exit(1)

    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx, timeout=30) as s:
        print("Connected! Authenticating...")
        s.login(SENDER, pwd)
        print("Authenticated! Sending...")
        s.sendmail(SENDER, [SENDER], msg.as_string())
        print(f"EMAIL SENT to {SENDER}!")
        print(f"Subject: {SUBJECT}")
        print("Check your inbox.")

if __name__ == "__main__":
    main()
