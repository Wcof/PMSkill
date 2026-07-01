---
name: pm-aiprd
description: 从 PMContext 生成给 AI 执行的 PRD——可执行规则 + 数据模型 + Agent Context + 验收标准 + 风险项，每条需求附 PMContext 追溯标记。Use when another skill needs Agent-executable PRD, or the user asks for AI-ready PRD, mentions 给 AI 的 PRD、可执行规则、Agent Context、ai-prd、自动化执行、技术契约.
---

# /pm-aiprd

> 你是一位资深产品经理，正在为 AI 执行团队撰写一份可执行的 PRD。核心原则：**AI 读了这个 PRD 应该能直接开始写代码，不需要再问问题**。参考模板来源：[PM Compass AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)。

从 PMContext 输出给 AI 的 PRD，带 Agent Context，供 Agent 执行。核心原则：**AI 读了这个 PRD 应该能直接开始写代码，不需要再问问题**。

## Purpose

从 PMContext 输出给 AI 的 PRD，带 Agent Context，供 Agent 直接执行。AI 读了这个 PRD 应该能直接开始写代码，不需要再问问题。

## Context

PMContext 已沉淀事实/假设/冲突/待确认。AI PRD 的职责是将这些转化为可执行契约——每条规则可直接落地为代码，[待确认] 项显式隔离不进入用户故事。

## Instructions

读取 `docs/pm-context/pm-context.md`。若不存在 → 🔴 STOP：提示先运行 `/pm-need`。

- [ ] PMContext 已读取且非空
- [ ] 概述/页面定义/全局约束/假设清单/风险项/信息缺口全部提取
- [ ] Agent Context（技术栈/目录结构/关键模块）已确认
- [ ] [待确认] 项隔离不进入用户故事
- [ ] 每条用户故事和规则后追加 `← PMContext: <章节>` 追溯标记
- [ ] 输出生成摘要：用户故事数/规则数 + [待确认]占比+警示

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的 AI PRD 部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（AI PRD） | 从 PMContext 生成给 AI 执行的 PRD，每条需求追溯到步骤 4 的决策 + 步骤 5 的风险已处理 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/aiprd-step6.md`。

**产出约束**：
- 必须产出**交付物清单**：每条需求追溯到步骤 4 的哪个决策 + 步骤 5 的哪个风险已处理
- 未追溯的交付物标 `[待确认]`，不得写成确定性要求
- 步骤 5 中 Launch-Blocking Tiger 必须在风险项章节有对应缓解措施
- [待确认] 项不得写入用户故事或实施规则

**依赖检查**：是否有未追溯的交付物？是否有步骤 5 中未处理的风险？

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

**审计三元组示例**：
`<依据集: [PMContext§用户登录事实, 步骤4决策"选择JWT方案"]> → [工具: /pm-aiprd, 规则: 追溯纪律] → [转换: PMContext事实"需登录才能访问"→用户故事US-1+可执行规则R-1] → <产出: US-1 + R-1 + ←PMContext:用户登录>`

## 流程链落盘

步骤 6（交付）产出完成后，写入中间工件：
- `docs/pm-context/.loop/aiprd-step6.md`（交付物清单 + 追溯映射 + 审计三元组）

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
从 PMContext 衍生，带场景和验收标准。格式：
1. As an <actor>, I want <feature>, so that <benefit>
   ← PMContext: <章节> | 审计: 依据源N + /pm-refine 8维之"维度"

## 实施规则（Rules）
从 PMContext 衍生，确定性要求。每条规则必须是 Agent 可直接执行的指令。
- R-<N>: <规则内容>
  ← PMContext: <章节> | 审计: 依据源N + /pm-refine 8维之"维度"

## 数据模型（Data）
关键实体和字段。

## 验收标准（Acceptance）
每个用户故事怎么算做完。步骤化格式：
```markdown
### US-<N>: <用户故事标题>
- **目标**：<验证什么>
- **前置条件**：<开始前需要什么>
- **步骤**：
  1. <操作>
  2. <操作>
  3. ...
- **预期结果**：<每步对应的预期>
- **边界场景**：<异常路径怎么处理>
```

## 风险项（Risks）
[待确认]/[假设]/[冲突] 标记的内容。每项标明：
- 标记类型
- 影响范围（哪些用户故事/规则受影响）
- 处理方式（"等待 PM 确认" / "按最乐观假设继续" / "需要备选方案"）

## 超出范围（Out of Scope）
明确不做的事，每条附排除理由。
```

## 待确认项处理规则

| PMContext 标记 | 占比阈值 | AI PRD 中的处理 |
|--------------|---------|---------------|
| `[事实]` | - | 直接写入，标注来源 `← PMContext: <章节>` |
| `[假设]` 置信度 ≥ 8 | - | 写入并在括号标注`（假设：PMContext 中 <内容>，置信度 N/10）`，可进入用户故事 |
| `[假设]` 置信度 5-7 | - | 写入实施规则但加 `⚠️ 假设项` 前缀，不进入验收标准 |
| `[假设]` 置信度 < 5 | - | 写入风险项章节，不进入用户故事或规则 |
| `[待确认]` | 占比 ≤ 30% | 写入风险项章节，标注"待 PM 确认"。**不写入用户故事或规则**——未确认项不能作为执行依据 |
| `[待确认]` | 占比 30%-50% | 同上 + PRD 顶部加 🟡 警示横幅"PRD 草案：含 N 项待确认" |
| `[待确认]` | 占比 > 50% | 同上 + 横幅升级为 🔴"PRD 不可执行：待确认占比过高" |
| `[冲突]` | - | 写入风险项章节，列出双方观点 + Agent 选定方向及理由，不进入用户故事 |

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext `[待确认]` 占比 > 50% | 输出 PRD 草案但不视为正式 PRD，顶部加 🔴 警示 | 标记为 `draft` 后缀 `ai-prd.draft.md`，不覆盖已有正式 PRD |
| Agent Context 需技术栈信息而 PMContext 中缺失 | 从 `package.json`/`pyproject.toml`/`Cargo.toml` 等配置文件读取，标注"来自项目扫描" | 全部缺失则技术栈标 `[待确认]`，不臆造 |
| PMContext 中 `[冲突]` 项涉及核心规则 | 不强行选定方向，规则章节标 `⚠️ 冲突项：见风险项章节` | 验收标准跳过该规则，提示 PM 先解决冲突 |
| ai-prd 与 human-prd 同源项出现分歧 | 以 PMContext 为准修正 ai-prd，标注修正项 | 仍不一致则 git diff 记录分歧供 PM 审计 |
| 用户故事无法追溯到 PMContext 事实 | 标 `[待确认]` 移入风险项章节，不进入用户故事列表 | 不阻塞，但必须在产物顶部汇总追溯失败项 |

## 关联增强

生成时确保每条需求都追溯到 PMContext 中的具体项，无来源的需求标 `[待确认]`。
在 ai-prd.md 中每条用户故事和规则后追加 `← PMContext: <章节>` 标记。

**🔴 CHECKPOINT** — 输出生成摘要：用户故事数/规则数 + [待确认]占比+警示 + 追溯失败项。

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 把 `[待确认]` 项写成确定性要求 | 执行 Agent 会当真，导致交付偏差 |
| 不追溯来源（每个需求要有 ← PMContext 标记） | AI 无法判断哪些来自事实、哪些是推断 |
| 在用户故事中混入技术实现细节 | 用户故事是做什么（what），不是怎么做（how） |
| 忽略边界场景（d3 缺失） | 执行 Agent 遇到异常路径会不知所措 |
| 把 Agent Context 塞给人类读者（human-prd 与 ai-prd 内容互换） | AI 要的东西和人要看的不同 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"经过分析得到" | 空话，必须写明是同义词推导/多对多实体映射/边界隔离分析之一（ADR 0008 §11） |

## 产出示例

`/pm-prd --skip-human 会员体系重构` → `prd/ai-prd.md` 概要：

```
# 会员体系重构 AI PRD

## Agent Context
- 技术栈: Node.js 18 + PostgreSQL 15 + Redis 7
- 目录: app/controllers/member*, app/models/member.rb
- 关键模块: MemberService (续费逻辑)、NotificationService (提醒推送)

## 用户故事
### US-1: 年付方案选择
As a 月付用户, I want to upgrade to 年付, so that 节省费用
- **验收标准**：
  1. 月付用户可在"续费页"切换年/月付 tab
  2. 年付价格必须 ≤ 月付 × 10
  3. 切换后已付月费按比例抵扣 ← [假设: 财务支持比例退款，8/10]

## 实施规则
[7 条可执行规则...]
```

### Further Reading

- [A Proven AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [How to Write a Product Requirements Document? The Best PRD Template.](https://www.productcompass.pm/p/prd-template) — 8 节模板参考

## 产出示例 · 延伸参考 · 实战提示

详见 [references/agent-prd-example.md](references/agent-prd-example.md)（给 AI 的 PRD 片段示例与可执行规则书写技巧）。

### 实战提示

- **[待确认] 大于 30% 标 🟡，大于 50% 标 🔴**：前者是草案，后者是不可执行
- **每条规则必须是可执行的**："确保用户体验良好"不叫规则，"按钮不小于 44px"才叫规则
- **Agent Context 不可省略**：技术栈/目录结构/关键模块位置是 AI 执行的前提
