---
name: auto-email-sender
description: |
  Send professional emails via Gmail SMTP with natural language content.

  Use when:
  - Sending job application emails
  - Generating content that reads human-written (no AI markers)
  - Automating email correspondence via Gmail SMTP

  Requires GMAIL_APP_PASSWORD. Default sender: alexandertianlin@gmail.com
---

# Auto Email Sender

Setup: export GMAIL_APP_PASSWORD=your16charcode

## Content Generation (Critical)
Read references/content_generation.md BEFORE writing email body.
AVOID: bullet points, perfect structure, skill listings, formulaic phrases.

## Send
python3 scripts/send_email.py --to "r@x.com" --subject "S" --body t.txt
python3 scripts/send_email.py --to "r@x.com" --subject "S" --body-text "Dear..." --attach r.docx
python3 scripts/send_email.py --from-file emails.json
