# Refine 模块指南

## 职责

把原始材料提炼为可追溯、可确认的结构化需求上下文。

## 核心约束

1. **必须区分事实和推断。**
2. 必须提取业务背景、业务目标、业务约束、设计决策。
3. 必须标记冲突点和待确认问题。
4. **禁止把 AI 推断写成确定事实。**
5. 每条关键内容必须有来源（来源材料 + 来源位置）。
6. 不允许隐藏冲突点。
7. 不允许跳过待确认问题。
8. 不允许删除重要背景。
9. 不允许凭空新增业务规则。

## 输入

- `docs/prd-helper/01-collect/` 下的原始材料

## 输出

输出到 `docs/prd-helper/02-refine/`：

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

## ID 命名约定

每条实体使用 `{前缀}_NNN` 格式（如 `fact_001`、`decision_002`）。

完整实体类型定义见 `scripts/lib/id_registry.py`。

## 验收条件

- 事实与 AI 推断严格分离
- 关键事实/决策/约束有来源材料与来源位置
- 冲突点与待确认问题明确记录
- 没有把推断写成事实
- 没有隐藏冲突点
- 没有跳过待确认问题
- 输出 `check.md`

## 逐文件验收条件

| 文件 | 验收条件 |
|------|----------|
| `facts.md` | 每个 fact 有事实内容、来源材料、来源位置、可信度和状态 |
| `background.md` | 背景摘要、业务现状、当前痛点、相关角色、来源说明和待确认问题完整 |
| `goals.md` | 每个 goal 有目标内容、目标类型、影响对象、来源材料、衡量方式和状态 |
| `decisions.md` | 每个 decision 有决策内容、原因、替代方案、影响范围、来源材料、来源位置和状态 |
| `constraints.md` | 每个 constraint 有约束内容、类型、影响对象、违反后果、来源材料、来源位置和状态 |
| `conflicts.md` | 每个 conflict 有冲突描述、双方观点、涉及来源、影响范围、决策人、状态和结论 |
| `questions.md` | 每个 question 有问题描述、产生原因、来源材料、影响范围、优先级、确认人和状态 |
| `assumptions.md` | 每个 assumption 有推断内容、来源材料、推断依据、不能确定原因、影响范围、是否进入生成文档和状态 |
| `check.md` | 使用 `02-refine-check-template.md`，并能引用 `check-refine.py` 的检查结果 |

## 检查

使用 `templates/02-refine-check-template.md` 生成 `check.md`。

检查要点：
- 信息分类检查（事实、背景、目标、决策、约束、冲突、问题、推断）
- 来源检查（关键事实/决策/约束/冲突有来源，推断已标记）
- 风险检查（无推断伪装事实、无隐藏冲突、无跳过问题、无删除背景、无凭空规则）

## 下一步

通过检查后进入 **Relate（关联）** 阶段。
