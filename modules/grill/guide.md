# PRD Discuss 模块指南

## 职责

`/prd-discuss` 是 PRD Helper 的需求研讨模式，用来在采集和精炼之间追问矛盾、模糊术语和未决问题。

它是辅助能力，不是第五个业务阶段。研讨结论必须回到 PRD Helper 主链路：进入 `02-refine/` 的事实、决策、冲突、问题、推断，或进入根目录 `CONTEXT.md` 的术语和关系说明。

## 前置条件

- `capture_mode` 必须为 `on`（已执行 `/prd-start`）
- 触发命令：`/prd-discuss`
- 已采集材料位于 `docs/prd-helper/01-collect/active/` 或 `docs/prd-helper/01-collect/passive/`

## 流程

### Phase 1: 扫描与呈现

1. 读取 `01-collect/active/` 和 `01-collect/passive/` 下的已采集材料。
2. 梳理矛盾点、模糊术语、未解决冲突、明显遗漏项。
3. 用清单向用户呈现发现，并询问本轮优先讨论哪一个问题。

不要一次抛出长问卷。优先从最影响后续精炼和关联的问题开始。

### Phase 2: 逐问逐答

进入研讨模式后，每轮只追问一个问题：

- 问题必须具体，能推动事实、决策、冲突、问题或推断归位。
- 每个问题都给出推荐答案或推荐判断，降低用户回答成本。
- 如果问题可以通过读已采集材料、`CONTEXT.md` 或 ADR 回答，先探索再提问。
- 用户回答后，立即说明这条结论应该沉淀到哪里。

### Phase 3: 沉淀结论

每条已确认结论必须归入一个明确去向：

| 结论类型 | 去向 |
|----------|------|
| 已确认事实 | `02-refine/facts.md` |
| 已做决策 | `02-refine/decisions.md` |
| 仍有分歧 | `02-refine/conflicts.md` |
| 需要继续确认 | `02-refine/questions.md` |
| AI 推断但未确认 | `02-refine/assumptions.md` |
| 术语定义或关系 | 根目录 `CONTEXT.md` |
| 难以逆转的真实权衡 | `docs/adr/` |

## 行为规则

### 挑战术语表

当用户使用的术语与项目 `CONTEXT.md` 冲突时，立即指出：

> `CONTEXT.md` 中把“X”定义为 Y，但你刚才的用法更像 Z。这里应以哪个为准？

### 模糊语言精炼

当用户使用模糊或重载术语时，提出精确的规范术语，并说明它会影响哪个精炼产物。

### 具体场景压力测试

讨论领域关系时，用具体场景测试边界。例如：角色不同、状态不同、异常发生、权限不足、数据缺失时，原说法是否仍成立。

### 交叉引用材料

当用户陈述与已采集材料、`CONTEXT.md` 或 ADR 不一致时，指出矛盾来源，并让用户选择以哪一个为准。

### 更新 CONTEXT.md

术语或关系澄清后，及时更新项目根目录的 `CONTEXT.md`。只写与产品上下文有关的概念，不写实现细节。

### 谨慎创建 ADR

只有同时满足以下条件时才提议创建 ADR：

1. 难以逆转：后续改变成本明显。
2. 没有上下文会令人惊讶：未来读者会问为什么。
3. 真实权衡：存在可行替代方案，且当前选择有明确原因。

## 产出物

| 产出 | 位置 | 说明 |
|------|------|------|
| 对话记录 | `01-collect/active/` | hooks 自动记录，无需手动处理 |
| 研讨摘要 | `docs/prd-helper/01-collect/grill/discussion-summary.md` | 研讨结束时生成 |
| 未解决问题 | `docs/prd-helper/01-collect/grill/open-questions.md` | 仅保留仍需确认的问题 |
| CONTEXT.md 更新 | 项目根目录 `CONTEXT.md` | 记录术语、关系和歧义澄清 |
| ADR | `docs/adr/` | 按需创建 |

## 状态

当前实现通过 `collect-state.md` 中的 `grill_mode` 字段跟踪研讨状态：

- `grill_mode: on` — 需求研讨进行中
- `grill_mode: off` — 未激活或已结束

`/prd-stop` 会结束主动采集，也应结束需求研讨并生成研讨摘要。
