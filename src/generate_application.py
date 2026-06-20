#!/usr/bin/env python3
"""Generate application packages for all target companies."""
import json, os, shutil

BASE = os.path.dirname(os.path.dirname(__file__))
APPS = os.path.join(BASE, "applications")
OUTPUTS = os.path.join(BASE, "outputs")

APPLICATIONS = [
    {"company": "小鹏机器人", "position": "VLM/VLA 大模型算法工程师",
     "platform": "飞书招聘", "url": "https://xiaopeng.jobs.feishu.cn/398875/m/position/7543105090077493550/detail", "priority": "高"},
    {"company": "超维动力智能", "position": "具身智能算法研究员 (VLA/多模态)",
     "platform": "猎聘", "url": "https://m.liepin.com/job/1977515313.shtml", "priority": "高"},
    {"company": "光象科技", "position": "具身智能算法工程师 (多模态大模型)",
     "platform": "猎聘", "url": "https://www.liepin.com/job/1982573277.shtml", "priority": "中"},
]

print("=" * 50)
print("Application Package Generator")
print("=" * 50)
print(f"\n{len(APPLICATIONS)} companies to apply:\n")
for app in APPLICATIONS:
    print(f"[{app["priority"]}] {app["company"]} - {app["position"]}")
    print(f"     URL: {app["url"]}")
print(f"\nOpen each URL in browser and follow the application process.")
