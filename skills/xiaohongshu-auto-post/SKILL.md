 ---
 name: xiaohongshu-auto-post
 description: |
   基于 white0dew/XiaohongshuSkills (3K stars) 的小红书自动发帖 Skill。
   支持图文/视频自动发布、多账号管理、浏览器自动化(CDP)。
 metadata:
   trigger: 发帖到小红书 / 小红书自动发帖 / 小红书发布
   source: white0dew/XiaohongshuSkills
   version: v1.0-baseline
 ---
 
 # 小红书自动发帖 Skill
 
 基于开源项目 white0dew/XiaohongshuSkills 封装的小红书自动发帖工具。
 
 ## 风险提示
 **使用本 Skill 进行小红书自动化，存在被平台风控、限流、封号的风险。**
 建议仅先在测试号上验证，控制发布频率，并对最终发布内容进行人工复核。
 
 ## 路径
 项目路径: C:\Users\tianl\Documents\Codex\tasks\task-xiaohongshu-auto-post\v1.0-feat-baseline-20260620\src
 
 ## 使用方法
 
 ### 1. 首次登录
 ```cmd
 cd /d C:\Users\tianl\Documents\Codex\tasks\task-xiaohongshu-auto-post\v1.0-feat-baseline-20260620\src\scripts
 python cdp_publish.py login
 ```
 
 ### 2. 发布图文
 ```cmd
 cd /d C:\Users\tianl\Documents\Codex\tasks\task-xiaohongshu-auto-post\v1.0-feat-baseline-20260620\src\scripts
 python publish_pipeline.py --headless ^
   --title "标题" ^
   --content "正文" ^
   --image-urls "https://example.com/image.jpg"
 ```
 
 ### 3. 更多功能
 详见项目 README.md
 
 ## 依赖
 - Python 3.10+
 - Google Chrome 浏览器
 - requests, websockets
