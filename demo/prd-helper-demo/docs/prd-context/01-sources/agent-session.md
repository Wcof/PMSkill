# Agent 对话摘要

## 基本信息

| 字段 | 内容 |
|------|------|
| 材料标题 | Agent 对话中的关键纠正 |
| 材料类型 | Agent 对话摘要 |
| 来源 | Claude Code 对话 |
| 记录时间 | 2024-01 |
| 记录人 | 产品经理 |
| 涉涉及模块 | 全局 |
| 后续处理建议 | 需要精炼 |

## 关键词

Agent对话, 纠正, Demo场景, 敏捷开发

## 原始内容

Agent 曾经把业务 Demo 场景误认为巡检机器人 Demo。

用户纠正：v0.1 Demo 的主角应该是 PRD helper 自身。

Agent 曾经建议缩减为最小 MVP。

用户纠正：当前采用敏捷开发，但仍希望完整流程闭环，不要缩减计划，只更正说明。

当前 PRDHelper 已经支持安装到目标项目 `.agents/skills/create-prd/`。

安装后会注入 AGENTS.md 和 CLAUDE.md。

PRD 产物默认写入目标项目 `docs/prd/`。

当前项目已有 README、SKILL.md、templates、prdctl.py、verify_release.py、showcases 和 test-prompts.json。
