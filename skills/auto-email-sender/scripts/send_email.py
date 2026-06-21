#!/usr/bin/env python3
import smtplib, ssl, os, sys, json, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SENDER = os.environ.get("GMAIL_SENDER", "alexandertianlin@gmail.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def get_password():
    pwd = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("EMAIL_PASS")
    if not pwd:
        try: pwd = getpass.getpass("Gmail App Password: ")
        except: pass
    if not pwd:
        print("ERROR: Set GMAIL_APP_PASSWORD environment variable")
        sys.exit(1)
    return pwd

def send_email(recipient, subject, body_text, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        fname = os.path.basename(attachment_path)
        part.add_header("Content-Disposition", f"attachment; filename="{fname}"")
        msg.attach(part)
    pwd = get_password()
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx, timeout=30) as s:
        s.login(SENDER, pwd)
        s.sendmail(SENDER, [recipient], msg.as_string())
    print(f"Sent to {recipient}: {subject}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--to")
    parser.add_argument("--subject")
    parser.add_argument("--body")
    parser.add_argument("--body-text")
    parser.add_argument("--attach")
    parser.add_argument("--from-file")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    if args.from_file:
        with open(args.from_file) as f:
            cfg = json.load(f)
        for email in cfg.get("emails", []):
            body = email.get("body", "")
            if email.get("body_file"):
                with open(email["body_file"]) as ff:
                    body = ff.read()
            send_email(email["to"], email["subject"], body, email.get("attach"))
    elif args.interactive:
        to = input("To: ")
        subject = input("Subject: ")
        print("Body (Ctrl+D to finish):")
        body = sys.stdin.read()
        send_email(to, subject, body)
    else:
        if not args.to or not args.subject:
            parser.print_help()
            sys.exit(1)
        body = args.body_text or (open(args.body).read() if args.body else "")
        send_email(args.to, args.subject, body, args.attach)
