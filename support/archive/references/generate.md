# 生成环节（Generate）

## 目标

生成环节负责基于采集、精炼和关联后的结果，生成结构化 PRD。

它不是凭空写文档，而是基于已有事实和关系生成。

核心目标：让不同角色拿到自己能用的文档。

## 生成文档类型

第一版至少生成六类文档：

1. 项目说明
2. 页面说明
3. 功能规则
4. 数据说明
5. 验收标准
6. Agent 上下文

## 输出目录

```
docs/prd-helper/04-generate/
```

## 输出结构

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

## 行为规范

1. 必须基于 refined 和 relations 生成，不允许凭空新增业务规则。
2. 必须保留待确认问题。
3. 每个页面必须有目标、区域、字段、操作、状态。
4. 每个规则必须有条件、步骤、异常、权限。
5. 每个数据对象必须有字段语义和关系。
6. 每个核心功能必须有验收标准。
7. 必须生成 Agent 可执行上下文。

## 模板

| 文档类型 | 模板 |
|---------|------|
| 项目说明 | `04-generate-overview-template.md` |
| 页面说明 | `04-generate-page-prd-template.md` |
| 功能规则 | `04-generate-rule-prd-template.md` |
| 数据说明 | `04-generate-data-prd-template.md` |
| 验收标准 | `04-generate-acceptance-template.md` |
| Agent 上下文 | `04-generate-agent-context-template.md` |
| 生成检查 | `04-generate-check-template.md` |

## Agent 上下文角色

| 角色 | 侧重 |
|------|------|
| 前端 | 页面说明、字段、交互、状态 |
| 后端 | 业务规则、数据对象、接口用途、权限 |
| 测试 | 验收标准、异常场景、状态流转 |
| 产品 | 项目全貌、决策记录、待确认问题 |

## 验收标准

生成环节完成必须满足：

1. 有项目说明。
2. 有页面说明。
3. 有功能规则。
4. 有数据说明。
5. 有验收标准。
6. 有 Agent 上下文。
7. 生成内容能追溯到精炼和关联结果。
8. 未把 AI 推断写成确定事实。
9. 未遗漏待确认问题。
10. 生成 `check.md`。
