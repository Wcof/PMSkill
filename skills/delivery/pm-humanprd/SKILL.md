---
name: pm-humanprd
description: 从 PMContext 生成给人阅读的 PRD。Use when the user asks for a human-readable PRD or review document.
---

# /pm-humanprd

从 PMContext 输出给人的 PRD，供人类阅读评审。

## 产物

写入 `docs/pm-context/prd/human-prd.md`，与 ai-prd.md 同源同骨架，但写法针对人类读者调整：

```markdown
# <需求名> PRD
## 概述（Overview）
完整背景 + 决策理由。
## 用户故事（User Stories）
自然语言，加业务价值说明。
## 实施规则（Rules）
决策表 + "为什么这样决定"。
## 数据模型（Data）
实体关系说明。
## 验收标准（Acceptance）
场景描述。
## 风险项（Risks）
标记 + 影响分析。
## 超出范围（Out of Scope）
列表 + 排除理由。
```

## 关联增强

生成时确保每条需求都追溯到 PMContext 中的具体项，无来源的需求标 `[待确认]`。
