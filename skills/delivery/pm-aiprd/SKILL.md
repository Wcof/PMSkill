---
name: pm-aiprd
description: 从 PMContext 生成给 AI 执行的 PRD。Use when another skill needs Agent-executable PRD, or the user asks for AI-ready PRD.
---

# /pm-aiprd

从 PMContext 输出给 AI 的 PRD，带 Agent Context，供 Agent 执行。

## 产物

写入 `docs/pm-context/prd/ai-prd.md`，结构如下：

```markdown
# <需求名> AI PRD
## 概述（Overview）
一段话说清楚要做什么、为什么。
## Agent Context
### 技术栈与约束
### 目录结构约定
### 关键模块位置
## 用户故事（User Stories）
从 PMContext 衍生，带场景和验收标准。每个用户故事格式：
1. As an <actor>, I want <feature>, so that <benefit>
## 实施规则（Rules）
从 PMContext 衍生，确定性要求。
## 数据模型（Data）
关键实体和字段。
## 验收标准（Acceptance）
每个用户故事怎么算做完。
## 风险项（Risks）
[待确认]/[假设]/[冲突] 标记的内容。
## 超出范围（Out of Scope）
明确不做的事。
```

## 关联增强

生成时确保每条需求都追溯到 PMContext 中的具体项，无来源的需求标 `[待确认]`。
