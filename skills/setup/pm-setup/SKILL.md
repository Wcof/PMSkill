---
name: pm-setup
description: 首次使用 PMSkill 时配置项目（目录/语言/Agent 规则）
disable-model-invocation: true
---

# /pm-setup

首次使用 PMSkill 时配置项目。运行一次即可，后续 Skill 自动读取配置。

## 流程

### 1. Explore

检查项目现有状态：

- `docs/pm-context/` 是否已存在？
- `AGENTS.md` / `CLAUDE.md` 是否有 PMSkill 配置？
- 当前 Agent 类型（Claude Code / Codex / Trae）

### 2. Ask

一次一个，等待反馈后再继续：

- **产物目录**：默认 `docs/pm-context/`，确认或自定义
- **语言偏好**：中文 / 英文 / 双语
- **Agent 类型**：Claude Code / Codex / Trae（决定写哪套规则）

### 3. Write

- 创建 `docs/pm-context/` 目录
- 在 `AGENTS.md` 或 `CLAUDE.md` 中写入极简 Agent 规则段：

```markdown
## PMSkill
- 领域术语：见 CONTEXT.md
- 产物目录：docs/pm-context/
- PMContext（唯一 Entity）：docs/pm-context/pm-context.md
```

不注册 hook——`/pm-collect` 从对话上下文直接收集，不需要拦截 Agent 会话。
