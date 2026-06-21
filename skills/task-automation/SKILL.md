# Skill: Task Automation (任务自动化)

> 基于 Makefile + .gitignore + .gitattributes 的项目级自动化规范。
> 源自 task-job-search 项目的最佳实践。

## 功能

- Makefile 一键命令（setup/report/clean/help）
- .gitignore 统一忽略规则（缓存、密钥、输出文件）
- .gitattributes 跨平台换行符规范
- requirements.txt 依赖锁定

## 标准 Makefile 模板

每个任务应包含一个 Makefile，提供以下标准目标：

| 目标 | 说明 | 默认 |
|------|------|------|
| setup | 环境配置（pip install） | 是 |
| clean | 清理缓存文件和临时输出 | 是 |
| help | 列出所有可用命令 | 是 |
| search | 运行核心搜索/采集逻辑 | 可选 |
| report | 生成报告 | 可选 |

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-21 | 来自 task-job-search GitHub 项目的最佳实践 |
