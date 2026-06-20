#!/bin/bash
set -e
echo "=== Tian Lin - One-Click Job Application ==="
DIR="$(cd "$(dirname "$0")" && pwd)"

# Check for Gmail App Password
if [ -z "$GMAIL_APP_PASSWORD" ]; then
  echo "Need GMAIL_APP_PASSWORD to send emails"
  echo "Run: GMAIL_APP_PASSWORD=xxxx bash $0"
  echo "Get password: Google Account > Security > App Passwords"
fi

# Send WeRide email
if [ -n "$GMAIL_APP_PASSWORD" ]; then
  echo "[1] Sending WeRide email..."
  export GMAIL_APP_PASSWORD
  python3 "$DIR/outputs/send_applications.py"
fi

# Open company application pages
echo "[2] Opening company pages..."
declare -A SITES
SITES[Dyson]="https://dyson.wd3.myworkdayjobs.com/dyson_careers/job/Singapore---St-James-Power-Station-Headquarters/Perception-Engineer--NPI-Robotic_JR34571/apply"
SITES[Intrinsic]="http://job-boards.greenhouse.io/intrinsicrobotics/jobs/5991885004"
SITES[ST_Engineering]="https://careers.stengg.com/talentcommunity/apply/1356001566/?locale=en_GB"
SITES[FieldAI]="https://jobs.lever.co/field-ai/f326c7a0-84ee-4f91-aa16-80281203e8d3/apply"
SITES[ASTAR]="https://careers.a-star.edu.sg/talentcommunity/apply/692/?locale=en_GB"
SITES[SIT]="https://www.timeshighereducation.com/unijobs/external-redirect-registration?JobId=411913&LinkSource=JobDetails"
SITES[XPeng]="https://xiaopeng.jobs.feishu.cn/398875/m/position/7543105090077493550/detail"

for name in "${!SITES[@]}"; do
  open "${SITES[$name]}" 2>/dev/null || true
  echo "  Opened: $name"
  sleep 1
done

# Show tracker
echo "[3] Application status:"
python3 "$DIR/v1.1-feat-apply-20260620/src/application_tracker.py" 2>/dev/null || true
echo "Done!"
