#!/usr/bin/env python3
"""Send job application emails via Gmail SMTP.
Requires Gmail App Password (Settings > Security > App Passwords).
Run: python3 send_applications.py
"""
import smtplib, ssl, sys, os, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SENDER = "alexandertianlin@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_email(recipient, subject, body, attachment_path=None):
    print(f"\nSending to: {recipient}")
    print(f"Subject: {subject}")
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)
    pwd = os.environ.get("GMAIL_APP_PASSWORD")
    if not pwd:
        pwd = getpass.getpass("Gmail App Password: ")
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as s:
        s.login(SENDER, pwd)
        s.sendmail(SENDER, [recipient], msg.as_string())
    print("  Sent!")

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "weride_application_email.txt"), "r", encoding="utf-8") as f:
        body = f.read()
    resume = "田霖简历_更新版.docx"
    if not os.path.exists(resume):
        resume = os.path.join(os.path.dirname(__file__), resume)
    send_email("alex.mah@weride.ai", "求职申请 - Perception Engineer - 田霖 (NTU硕士, 2026年12月毕业)", body, resume if os.path.exists(resume) else None)
