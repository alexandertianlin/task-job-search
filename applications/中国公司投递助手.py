
import sys, io, json, os, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUTPUT_DIR = r'C:\Users\tianl\Documents\Codex\2026-06-20\files-mentioned-by-the-user-docx\outputs\applications'
RESUME_PATH = r'C:\Users\tianl\Documents\Codex\2026-06-20\files-mentioned-by-the-user-docx\outputs\田霖简历_更新版.docx'

def generate_application_package():
    print("=" * 50)
    print("田霖 - 中国公司求职投递包生成器")
    print("=" * 50)
    
    apps = [
        {
            "company": "小鹏机器人",
            "position": "VLM/VLA 大模型算法工程师 (26届校招)",
            "platform": "飞书招聘系统",
            "url": "https://xiaopeng.jobs.feishu.cn/398875/m/position/7543105090077493550/detail",
            "cover_letter": os.path.join(OUTPUT_DIR, "小鹏机器人_VLM_VLA_求职信.md"),
            "status": "待投递",
            "priority": "高优先"
        },
        {
            "company": "超维动力智能",
            "position": "具身智能算法研究员 (VLA/多模态基础模型)",
            "platform": "猎聘网",
            "url": "https://m.liepin.com/job/1977515313.shtml",
            "cover_letter": os.path.join(OUTPUT_DIR, "超维动力智能_VLA_求职信.md"),
            "status": "待投递",
            "priority": "高优先"
        },
        {
            "company": "光象科技",
            "position": "具身智能算法工程师/研究员（多模态大模型方向）",
            "platform": "猎聘网",
            "url": "https://www.liepin.com/job/1982573277.shtml",
            "cover_letter": os.path.join(OUTPUT_DIR, "光象科技_具身智能_求职信.md"),
            "status": "待投递",
            "priority": "中优先"
        }
    ]
    
    print(f"\n共 {len(apps)} 个待投递岗位\n")
    
    for app in apps:
        print(f"[{app['priority']}] {app['company']} - {app['position']}")
        print(f"    平台: {app['platform']}")
        print(f"    链接: {app['url']}")
        print(f"    求职信: {app['cover_letter']}")
        print()
    
    print("投递步骤:")
    print("1. 打开各公司投递链接")
    print("2. 上传简历PDF")
    print("3. 填写个人信息")
    print("4. 附上求职信中对应内容")
    print("5. 提交申请")
    
    # Save application manifest
    manifest_path = os.path.join(OUTPUT_DIR, "application_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)
    print(f"\n清单已保存: {manifest_path}")

generate_application_package()
