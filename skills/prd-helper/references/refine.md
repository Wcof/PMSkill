# 精炼环节（Refine）

## 目标

精炼环节负责对采集到的原始材料进行清洗、压缩、提取和分类。

它不是简单摘要，而是把混乱信息整理成可确认、可追溯、可复用的需求上下文。

核心目标：把原始沟通变成结构化需求事实。

## 处理内容

精炼环节需要提取：

1. 需求事实
2. 业务背景
3. 业务目标
4. 业务约束
5. 设计决策
6. 冲突点
7. 待确认问题
8. AI 推断项
9. 证据来源
10. 可信度

## 输出目录

```
docs/prd-helper/02-refine/
```

## 输出文件

| 文件 | 用途 | 模板 |
|------|------|------|
| `facts.md` | 需求事实清单 | `02-refine-facts-template.md` |
| `background.md` | 业务背景 | `02-refine-background-template.md` |
| `goals.md` | 业务目标 | `02-refine-goals-template.md` |
| `decisions.md` | 设计决策记录 | `02-refine-decisions-template.md` |
| `constraints.md` | 业务约束清单 | `02-refine-constraints-template.md` |
| `conflicts.md` | 冲突点清单 | `02-refine-conflicts-template.md` |
| `questions.md` | 待确认问题清单 | `02-refine-questions-template.md` |
| `assumptions.md` | AI 推断项清单 | `02-refine-assumptions-template.md` |
| `check.md` | 精炼检查 | `02-refine-check-template.md` |

## 行为规范

1. 必须区分事实和推断。
2. 必须提取业务背景、业务目标、业务约束、设计决策。
3. 必须标记冲突点和待确认问题。
4. 禁止把 AI 推断写成确定事实。
5. 每条关键内容必须有来源。
6. 每条关键内容必须有可信度标注。

## 验收标准

精炼环节完成必须满足：

1. 产出 facts。
2. 产出 background。
3. 产出 goals。
4. 产出 decisions。
5. 产出 constraints。
6. 产出 conflicts。
7. 产出 questions。
8. 产出 assumptions。
9. 明确事实和 AI 推断分离。
10. 生成 `check.md`。
