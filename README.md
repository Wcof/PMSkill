# PRD Helper Skill Kit

![PRD Helper Skill Kit workflow](docs/prd-helper-skill-kit-flow.svg)

## 介绍

PRD Helper Skill Kit 是 PRD helper 的通用 Agent Skill 套件，用 Markdown 工作流把产品沟通、会议纪要、原型说明、客户反馈和 Agent 对话沉淀为可追溯、可复用、可检查的产品上下文。

它的核心流程是：采集原始材料，精炼事实、背景、目标、决策、约束、冲突、问题和 AI 推断，建立需求与页面、功能、规则、数据、验收之间的关系，生成角色化 PRD 和 Agent 上下文，最后输出检查结果与 Context Delta。

```text
01-collect → 02-refine → 03-relate → 04-generate → 05-check → Context Delta
```

项目只做 Skill、模板、检查规则、工具适配和 demo，不做 UI、后台、数据库或 SaaS 平台。

## 怎么用

1. 把 `skills/prd-helper/` 复制到目标项目的 `.agents/skills/prd-helper/`、`.claude/skills/prd-helper/` 或对应 Agent 工具的 Skill 目录。
2. 按使用工具复制 `adapters/` 里的适配说明，例如 Codex 使用 `adapters/codex/AGENTS.md`，Claude Code 使用 `adapters/claude-code/CLAUDE.md`，Trae 使用 `adapters/trae/project_rules.md`。
3. 准备会议纪要、聊天记录、原型说明、客户反馈或 Agent 对话摘要，让 Agent 使用 `prd-helper` Skill 处理。
4. 在目标项目的 `docs/prd-helper/` 查看输出：`01-collect`、`02-refine`、`03-relate`、`04-generate` 和 `05-check`。
5. 可运行检查脚本验证 demo：

```bash
python3 skills/prd-helper/scripts/check-structure.py demo/robot-inspection-demo/docs/prd-helper
python3 skills/prd-helper/scripts/check-relations.py demo/robot-inspection-demo/docs/prd-helper
python3 skills/prd-helper/scripts/check-generated.py demo/robot-inspection-demo/docs/prd-helper
```
