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
    pwd = password or os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("EMAIL_PASS")
    if not pwd:
        try: pwd = getpass.getpass("Gmail App Password: ")
        except: pass
    if not pwd:
        print("ERROR: Set GMAIL_APP_PASSWORD environment variable")
        sys.exit(1)
    return pwd

def _send_smtp(sender, pwd, recipient, msg):
    """Send via SMTP. Auto-tries SSL(465) then STARTTLS(587)."""
    import ssl
    last_err = None
    for port, use_ssl in [(465, True), (587, False)]:
        try:
            ctx = ssl.create_default_context()
            if use_ssl:
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ctx, timeout=30) as s:
                    s.login(sender, pwd)
                    s.sendmail(sender, [recipient], msg.as_string())
            else:
                with smtplib.SMTP("smtp.gmail.com", port, timeout=30) as s:
                    s.starttls(context=ctx)
                    s.login(sender, pwd)
                    s.sendmail(sender, [recipient], msg.as_string())
            return
        except Exception as e:
            last_err = e
            continue
    raise last_err

def send_email(recipient, subject, body_text, attachment_path=None, password=None):
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
    _send_smtp(SENDER, pwd, recipient, msg)
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
