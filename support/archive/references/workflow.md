# PRD Helper Workflow

## Overview

PRD Helper Skill Kit 的核心工作流是四个业务环节加一个横向质量机制。

```
采集 → 精炼 → 关联 → 生成
         ↕         ↕         ↕         ↕
       检查       检查       检查       检查
```

## 环节一：采集（Collect）

### 目标

尽量不让原始上下文丢失。

### 行为规范

1. 不判断、不总结、不直接生成 PRD。
2. 只负责把信息留下来，并按统一结构归档。
3. 保留原始含义，不提前改写成结论。

### 采集内容类型

- 产品经理口述
- 会议纪要
- 聊天记录
- 客户反馈
- 评审意见
- 内部讨论结论
- 原型说明
- 页面截图描述
- Agent 对话摘要
- 历史 PRD
- 历史方案
- 旧系统说明
- 研发实现补充说明
- 测试反馈
- 变更说明

### 输出目录

```
docs/prd-helper/01-collect/
```

### 必须输出

- 每份材料一个文件，使用 `01-collect-source-template.md` 模板
- `check.md` 采集检查结果

---

## 环节二：精炼（Refine）

### 目标

把混乱、重复、口语化、不完整的原始沟通，变成产品经理可以确认、研发可以理解、Agent 可以复用的干净上下文。

### 行为规范

1. 必须区分事实和推断。
2. 必须提取业务背景、业务目标、业务约束、设计决策。
3. 必须标记冲突点和待确认问题。
4. 禁止把 AI 推断写成确定事实。
5. 每条关键内容必须有来源。

### 输出目录

```
docs/prd-helper/02-refine/
```

### 输出文件

| 文件 | 用途 | 模板 |
|------|------|------|
| `facts.md` | 需求事实 | `02-refine-facts-template.md` |
| `background.md` | 业务背景 | `02-refine-background-template.md` |
| `goals.md` | 业务目标 | `02-refine-goals-template.md` |
| `decisions.md` | 设计决策 | `02-refine-decisions-template.md` |
| `constraints.md` | 业务约束 | `02-refine-constraints-template.md` |
| `conflicts.md` | 冲突点 | `02-refine-conflicts-template.md` |
| `questions.md` | 待确认问题 | `02-refine-questions-template.md` |
| `assumptions.md` | AI 推断 | `02-refine-assumptions-template.md` |
| `check.md` | 精炼检查 | `02-refine-check-template.md` |

---

## 环节三：关联（Relate）

### 目标

让需求、页面、功能、规则、数据和验收之间不再断链。

### 行为规范

1. 每个需求事实必须关联到页面或功能。
2. 每个功能必须关联到业务规则。
3. 每个业务规则必须关联到数据对象。
4. 每个页面必须关联到验收标准。
5. 待确认问题必须关联影响范围。
6. 不允许存在孤立需求、孤立页面、孤立规则。

### 关联关系

```
需求事实 → 页面
需求事实 → 功能
功能 → 业务规则
业务规则 → 数据对象
页面 → 字段
页面 → 操作
页面 → 接口用途
页面 → 验收标准
业务规则 → 异常场景
待确认问题 → 影响范围
Agent 对话增量 → 相关 PRD 文件
```

### 输出目录

```
docs/prd-helper/03-relate/
```

### 输出文件

| 文件 | 用途 | 模板 |
|------|------|------|
| `page-map.md` | 页面关联 | `03-relate-page-map-template.md` |
| `feature-map.md` | 功能关联 | `03-relate-feature-map-template.md` |
| `rule-map.md` | 规则关联 | `03-relate-rule-map-template.md` |
| `data-map.md` | 数据关联 | `03-relate-data-map-template.md` |
| `acceptance-map.md` | 验收关联 | `03-relate-acceptance-map-template.md` |
| `context-map.md` | 上下文总关联 | `03-relate-context-map-template.md` |
| `check.md` | 关联检查 | `03-relate-check-template.md` |

---

## 环节四：生成（Generate）

### 目标

基于已经确认和关联过的上下文，生成可信、可执行、可审计的 PRD 和 Agent 上下文。

### 行为规范

1. 必须基于 refined 和 relations 生成，不允许凭空新增业务规则。
2. 必须保留待确认问题。
3. 每个页面必须有目标、区域、字段、操作、状态。
4. 每个规则必须有条件、步骤、异常、权限。
5. 每个数据对象必须有字段语义和关系。
6. 每个核心功能必须有验收标准。
7. 必须生成 Agent 可执行上下文。

### 输出目录

```
docs/prd-helper/04-generate/
```

### 输出结构

```
04-generate/
├── overview/
│   └── project-overview.md
├── pages/
│   └── {page-name}.md
├── rules/
│   └── {rule-name}.md
├── data/
│   └── {data-name}.md
├── acceptance/
│   └── {feature-name}.md
├── agent-context/
│   ├── frontend-context.md
│   ├── backend-context.md
│   ├── test-context.md
│   └── product-review-context.md
└── check.md
```

---

## 检查机制（Check）

检查不是第五个业务环节，而是贯穿四个环节的质量门禁。

### 检查流程

```
采集后检查 → 01-collect/check.md
精炼后检查 → 02-refine/check.md
关联后检查 → 03-relate/check.md
生成后检查 → 04-generate/check.md
最终总检查 → 05-check/
```

### 详细检查规则

参见 `check-rules.md`。

---

## Context Delta

每次完成任务后，必须输出 Context Delta。

输出文件：`docs/prd-helper/05-check/context-delta.md`

参见 `context-delta.md`。
