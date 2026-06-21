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
## Key Improvements (from MacBook optimization)

### Dual Port Fallback
- Auto-tries SMTP_SSL(465) first, falls back to STARTTLS(587)
- Handles restrictive networks (corporate firewalls, VPNs)

### CLI Interface (auto_email.py)
- `python scripts/auto_email.py setup` - Interactive configuration
- `python scripts/auto_email.py list` - List targets and status
- `python scripts/auto_email.py send` - Send all pending emails
- `python scripts/auto_email.py status` - View send history

### HTML Email Support
- Markdown cover letters are converted to professional HTML emails
- Includes sender info footer with date

### Send Log & Config
- Per-target send tracking with timestamps
- Config file: config/email_targets.json
- Log file: outputs/email_send_log.json

### Improved Cover Letters (references/cover_letter_examples/)
- All letters have TWO versions: natural + structured
- Natural versions: NO bullet points, NO skill lists, NO "此致敬礼"
- Intrinsic letter: formal + casual English
- WeRide letters: both Chinese and English, natural versions
- 小鹏机器人: stripped down to pure natural language

### Password Security
- Priority: env var > config file > prompt
- Safer to use: export GMAIL_APP_PASSWORD=your16charcode
