#!/usr/bin/env python3
"""Job application tracker for task-job-search v1.1."""
import json, os, sys
from datetime import datetime

APPS = [
    {"id":1, "company":"Dyson Singapore", "title":"Perception Engineer", "status":"pending", "platform":"MyWorkDay"},
    {"id":2, "company":"Intrinsic (Google)", "title":"Software Engineer, Perception", "status":"pending", "platform":"Greenhouse"},
    {"id":3, "company":"A*STAR ARTC", "title":"Senior Research Scientist (Embodied AI)", "status":"pending", "platform":"SuccessFactors"},
    {"id":4, "company":"SIT Singapore", "title":"Research Fellow (Humanoid Robotics)", "status":"pending", "platform":"THE", "deadline":"2026-07-08"},
    {"id":5, "company":"小鹏机器人", "title":"VLM/VLA 大模型算法工程师", "status":"pending", "platform":"飞书"},
    {"id":6, "company":"WeRide", "title":"Perception Engineer", "status":"email_ready", "platform":"Email"},
    {"id":7, "company":"超维动力智能", "title":"具身智能算法研究员", "status":"pending", "platform":"猎聘"},
    {"id":8, "company":"NVIDIA", "title":"Research Scientist (Embodied Agent)", "status":"pending", "platform":"MyWorkDay"},
    {"id":9, "company":"ST Engineering", "title":"Embodied AI Engineer", "status":"pending", "platform":"SuccessFactors"},
    {"id":10, "company":"FieldAI", "title":"Robotics AI Engineer", "status":"form_filled", "platform":"Lever"},
    {"id":11, "company":"Intrinsic (Google)", "title":"Deep Learning Engineer, Perception", "status":"pending", "platform":"Greenhouse"},
    {"id":12, "company":"A*STAR I2R", "title":"(Senior) Scientist, Robotics & Autonomous Systems", "status":"pending", "platform":"SuccessFactors"},
    {"id":13, "company":"A*STAR SIMTech", "title":"(Senior) Research Scientist (Adaptive Robotics)", "status":"pending", "platform":"SuccessFactors"},
    {"id":14, "company":"Grab", "title":"Senior SDE, Perception (Robotics)", "status":"pending", "platform":"Grab Careers"},
    {"id":15, "company":"Jabil Circuit", "title":"Senior/Staff CV & AI Algorithm Engineer", "status":"pending", "platform":"MyWorkDay"},
    {"id":16, "company":"OKX", "title":"Senior/Staff Engineer, AI Agent Development", "status":"pending", "platform":"Greenhouse"},
]

TRACKER_FILE = os.path.join(os.path.dirname(__file__), "..", "outputs", "application_tracker.json")

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return APPS

def save_tracker(apps):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)

def show_status():
    apps = load_tracker()
    print(f"\n{'='*60}")
    print(f"Job Application Tracker - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    for a in apps:
        status_icon = {"pending":"⬜", "email_ready":"📧", "form_filled":"📝", "submitted":"✅", "rejected":"❌", "interview":"🎯"}
        icon = status_icon.get(a.get("status","pending"), "⬜")
        dl = f" ⏰{a['deadline']}" if a.get("deadline") else ""
        print(f"  {icon} [{a['id']:2d}] {a['company']:25s} | {a['title'][:40]:40s} | {a['platform']}{dl}")
    
    stats = {"pending":0, "email_ready":0, "form_filled":0, "submitted":0}
    for a in apps:
        s = a.get("status","pending")
        if s in stats: stats[s] += 1
    print(f"\n📊 待投递: {stats['pending']} | 邮件就绪: {stats['email_ready']} | 已填表: {stats['form_filled']} | 已提交: {stats['submitted']}")

def mark_submitted(app_id):
    apps = load_tracker()
    for a in apps:
        if a["id"] == app_id:
            a["status"] = "submitted"
            a["submitted_at"] = datetime.now().isoformat()
            save_tracker(apps)
            print(f"✅ {a['company']} - {a['title']} marked as submitted")
            return
    print(f"❌ Application {app_id} not found")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "submit":
        mark_submitted(int(sys.argv[2]))
    else:
        show_status()
        print(f"\n用法: python {sys.argv[0]} submit <id>  # 标记已提交")
