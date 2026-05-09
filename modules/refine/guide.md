# Refine 模块指南

## 职责

把原始材料提炼为可追溯、可确认的结构化需求上下文。

精炼模块只负责把材料说清楚、分清楚、标清楚。它不建立页面/规则/数据/验收链路，也不生成 PRD 文档。

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
10. 必须区分 **Strong Trace** 与 **Weak Trace**：确定性内容必须有 `source_id + path + quote/paraphrase + locator`。
11. **Weak Trace** 只能进入风险或待确认区，不能进入确定性 PRD 或 Agent Context 要求。

## 产物边界

| 产物 | 放什么 | 不放什么 |
|------|--------|----------|
| `facts.md` | 来源中明确出现、可被引用的需求事实 | AI 猜测、未来建议、未确认规则 |
| `background.md` | 业务现状、痛点、角色、上下文背景 | 页面结构、接口设计、验收条款 |
| `goals.md` | 用户或业务想达成的目标 | 实现方案细节 |
| `decisions.md` | 已做出的产品或设计决策，以及原因和替代方案 | 仍待确认的问题 |
| `constraints.md` | 明确的业务、合规、技术或时间约束 | 普通偏好或建议 |
| `conflicts.md` | 来源之间互相矛盾或尚未统一的说法 | 已解决且无影响的历史分歧 |
| `questions.md` | 需要用户、产品或业务继续确认的问题 | Agent 自己已经能从来源中确认的内容 |
| `assumptions.md` | AI 基于来源做出的推断，并说明不能确定的原因 | 被写成确定事实的推断 |

如果一条信息既像事实又像推断，默认放入 `assumptions.md`，并在 `questions.md` 中补一个确认问题。

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

确定性条目还必须包含可定位来源锚点：

```markdown
- source_id：
- path：
- quote / paraphrase：
- locator：
```

缺少 locator、quote/paraphrase、source_id 或 path 的内容属于 Weak Trace。

## 检查

使用 `templates/02-refine-check-template.md` 生成 `check.md`。

检查要点：
- 信息分类检查（事实、背景、目标、决策、约束、冲突、问题、推断）
- 来源检查（关键事实/决策/约束/冲突有来源，推断已标记，并区分 Strong Trace / Weak Trace）
- 风险检查（无推断伪装事实、无隐藏冲突、无跳过问题、无删除背景、无凭空规则）

精炼通过只代表材料已经被正确分类和来源化，不代表关系完整，也不代表可以直接生成 PRD。

## 下一步

通过检查后进入 **Relate（关联）** 阶段。
