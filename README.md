# task-job-search

简历匹配职位搜索与自动投递系统
Resume-based job search and auto-application assistant

## 概述

基于田霖的个人简历（NTU信号处理与机器学习硕士，2026年12月毕业），
自动搜索匹配的具身智能、计算机视觉、AI Agent方向职位，并提供投递支持。

## 候选人画像

- **教育**: 南洋理工大学（NTU）信号处理与机器学习硕士（2026年12月毕业）
- **研究方向**: 具身智能、VLA模型、多模态基础模型
- **核心技能**: Python/PyTorch, ONNX/TensorRT, LLM Agents, STM32, Unity, GCP GPU
- **经验**: NTU DeCLaRe Lab研究员、手势识别/传感器融合工程师、AI Agent工程师

## 目录结构

```
task-job-search/
├── scripts/          # Shell脚本（Mac/Linux兼容）
├── src/              # Python源码
├── docs/             # 文档
├── applications/     # 求职信 & 投递资料
├── outputs/          # 输出报告
├── README.md         # 本文件
├── Makefile          # 自动化命令
└── .gitignore
```

## Quick Start

```bash
# 1. 环境配置
make setup

# 2. 查看职位搜索结果
cat outputs/job_search_report.md

# 3. 生成投递包
python3 src/generate_application.py
```

## 投递优先级

| 优先级 | 公司 | 职位 | 链接 |
|--------|------|------|------|
| 🥇 | Dyson Singapore | Perception Engineer | [Apply](https://dyson.wd3.myworkdayjobs.com/dyson_careers/job/Singapore/Perception-Engineer--NPI-Robotic_JR34571/apply) |
| 🥇 | Intrinsic (Google) | Software Engineer, Perception | [Apply](http://job-boards.greenhouse.io/intrinsicrobotics/jobs/5991885004) |
| 🥇 | A*STAR ARTC | Senior Research Scientist (Embodied AI) | [Apply](https://careers.a-star.edu.sg/talentcommunity/apply/692/) |
| 🥇 | SIT Singapore | Research Fellow (Humanoid Robotics) | [Apply](https://www.timeshighereducation.com/unijobs/external-redirect-registration) |
| 🥇 | 小鹏机器人 | VLM/VLA大模型算法工程师 | [Apply](https://xiaopeng.jobs.feishu.cn/398875/m/position/7543105090077493550/detail) |
| 🥇 | WeRide | Perception Engineer | Email: alex.mah@weride.ai |

## 依赖

- Python 3.8+
- `requests` library (for web search)
- 网络连接
