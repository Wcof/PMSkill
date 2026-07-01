---
name: pm-premortem
description: 从 PMContext 假设上线失败并倒推风险，产出 Tiger（真实风险）/Paper Tiger（过虑）/Elephant（未讨论）三分 + 行动计划，与假设清单交叉检查。Use when preparing for launch, stress-testing a plan, or the user mentions Pre-Mortem、风险分析、risk analysis、上线前、压力测试、Tiger、行动计划、launch readiness.
---

# /pm-premortem

> 你是一位资深产品经理，正在为一个即将上线的产品做 Pre-Mortem。方法论源自 [PM Compass 的 Pre-Mortem 实践](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)（Meta/Instagram 团队使用）：**假设上线失败，然后倒推为什么**。

从 PMContext 出发，假设产品上线失败，倒推风险并分类，产出行动计划。PMContext 的风险分析 View，和 PRD/草图平级。

## Purpose

从 PMContext 出发，假设产品上线失败，倒推风险并分类，产出行动计划。Pre-Mortem 不是列全部风险而是筛可行动风险。

## Context

产品即将上线。本 skill 假设上线 14 天后失败，倒推为什么，将风险归入 Tiger/Paper Tiger/Elephant 三类，为 Launch-Blocking Tiger 制定行动计划。

## Instructions

读取 `docs/pm-context/pm-context.md`。若不存在，提示先运行 `/pm-need`。

- [ ] PMContext 已读取且非空
- [ ] 假设清单和风险项全部提取
- [ ] 假设「上线 14 天后失败」并倒推原因
- [ ] Tiger 有负责人+截止日期+行动
- [ ] Paper Tiger 说明为何不是真风险
- [ ] Elephant 说明为何暂不处理
- [ ] 低置信度假设（≤5）交叉检查升级为 Tiger
- [ ] Tiger 不超过 5 个，超出的降级为 Fast-Follow

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 5（风险）：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 5. 风险 | 假设上线失败倒推风险，按步骤 4 决策逐条检查"如果这个决策错了会怎样"，产出 Tiger/Paper Tiger/Elephant 三分 + 行动计划 | 回灌假设清单升级 |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/premortem-step5.md`。
达阈值的关键信息自动回灌到 PMContext 对应 heading（不开新 heading、走现有标记体系）。
每项产出必须附带审计三元组（依据集 → 工具/技术 → 产出），完整版落 `.loop/`，摘要回灌决策日志。

**产出约束**：
- 必须产出**风险清单**：按步骤 4 的决策逐条检查"如果这个决策错了会怎样"
- 风险必须覆盖步骤 4 的**所有决策点**，遗漏决策点则触发自愈
- Tiger 不超过 5 个，超出的降级为 Fast-Follow
- PMContext 中置信度 ≤ 5 的假设必须逐一交叉检查，假设失败可能导致上线失败的升级为 Tiger
- 每个风险项必须追溯到 PMContext 中的具体事实/规则/假设

**依赖检查**：风险是否覆盖步骤 4 的所有决策点？遗漏则补

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

**审计三元组示例**：
`<依据集: [步骤4决策D1, PMContext假设H3(置信度4)]> → [工具: /pm-premortem, 方法: Pre-Mortem倒推] → [转换: 决策D1"选择激进方案"失效路径分析→内存溢出→服务崩溃→上线失败] → <产出: Tiger风险"内存溢出导致服务不可用" + Launch-Blocking>`

## 流程

### 1. 读取 PMContext

理解产品目标、用户场景、规则、验收标准、全局约束、假设清单、风险项。

### 2. 假设失败

**Think Step by Step**：
1. 想象产品上线 14 天后失败了——用户不采用、指标没达标、出了事故
2. 问自己：
   - 什么出了错？
   - 我们遗漏了什么？
   - 我们对什么过度自信了？
3. 对每个潜在失败，追问"为什么"至少 3 层（5-Why 根因分析）：
   - 失败表象 → 为什么发生 → 根本原因 → 哪个假设/决策导致了根因
4. 将每条根因追溯到 PMContext 中的具体决策点或假设项

### 3. 分类风险

对每个潜在失败，归入三类：

**Tiger（真风险）**：有证据/逻辑支撑、可能真正阻断项目的风险
- 需要行动
- 应该让你睡不着

**Paper Tiger（纸老虎）**：表面看起来严重、但实际不太可能发生的风险
- 不值得投入大量资源
- 值得记录以对齐干系人认知

**Elephant（房间里的大象）**：团队没有充分讨论、但可能真实存在的风险
- 无人提及的隐忧
- 需要在上线前调查

**风险覆盖 8 域**（扩展自 Teresa Torres 4 核心产品风险 + 新产品 4 域）：

| # | 风险域 | 核心追问 | 适用场景 |
|---|--------|---------|---------|
| 1 | **Value** | 用户会为此付费/持续使用吗？ | 所有产品 |
| 2 | **Usability** | 用户能搞懂怎么用吗？认知负荷可接受吗？ | 所有产品 |
| 3 | **Viability** | 能卖出去/能规模化/合规吗？ | 所有产品 |
| 4 | **Feasibility** | 当前技术能实现吗？集成可行吗？ | 所有产品 |
| 5 | **Ethics** | 应该做吗？对用户有潜在危害吗？ | AI 驱动/数据产品 |
| 6 | **Go-to-Market** | 有渠道吗？能说服用户试用吗？时机对吗？ | 新产品/新市场 |
| 7 | **Strategy & Objectives** | 竞争对手能复制吗？PESTLE 因素考虑了吗？ | 战略级决策 |
| 8 | **Team** | 有对的人/工具吗？团队能撑到上线吗？ | 新团队/紧工期 |

每个 Tiger/Paper Tiger/Elephant 必须标注所属风险域，确保 8 域全覆盖。

### 4. Tiger 紧急度分级

**Launch-Blocking**：上线前必须解决
- 例：核心功能不可用、合规阻断、关键客户依赖未满足

**Fast-Follow**：上线后 30 天内必须解决
- 例：性能问题、次要功能不完整

**Track**：上线后监控，出问题再解决
- 例：nice-to-have 功能、边缘场景

### 5. 行动计划

为每个 Launch-Blocking Tiger 制定：
- 风险描述
- 缓解措施
- 负责人/角色
- 决策/完成日期

### 6. 与 PMContext 假设清单交叉

将 PMContext 中置信度 ≤ 5 的 `[假设]` 项逐一检查：
- 若假设失败会导致上线失败 → 升级为 Tiger
- 若假设失败影响有限 → 维持 Paper Tiger 或 Track

## 流程链落盘

步骤 5（风险）产出完成后，写入中间工件：
- `docs/pm-context/.loop/premortem-step5.md`（风险清单 + Tiger/Paper Tiger/Elephant 分类 + 行动计划 + 假设交叉检查 + 审计三元组）

## 产物，结构：

```markdown
# Pre-Mortem: <需求名>

## 假设场景
产品上线 14 天后失败。以下是我们认为可能出错的地方。

## Tigers（真风险）
| 风险 | 紧急度 | 缓解措施 | 负责人 | 完成日期 |
|------|--------|---------|--------|---------|
| ... | Launch-Blocking / Fast-Follow / Track | ... | ... | ... |

## Paper Tigers（纸老虎）
| 风险 | 为什么不太可能发生 |
|------|------------------|
| ... | ... |

## Elephants（房间里的大象）
| 风险 | 调查方式 |
|------|------------|
| ... | ... |

## 行动计划（Launch-Blocking Tigers）
| 风险 | 缓解措施 | 负责人 | 完成日期 |
|------|---------|--------|---------|
| ... | ... | ... | ... |

## 假设清单交叉检查
| PMContext 假设 | 置信度 | 假设失败后果 | 风险升级 |
|--------------|--------|------------|---------|
| ... | ≤5 | ... | Tiger / 维持 |
```

**🔴 CHECKPOINT** — 产物落盘后，展示摘要：
- Tiger 数量（Launch-Blocking / Fast-Follow / Track）
- Paper Tiger 数量
- Elephant 数量
- 假设升级为 Tiger 的数量

等待用户确认是否采纳行动计划。

## 关联增强

每个风险项追溯到 PMContext 中的具体事实/规则/假设，无来源的风险标 `[假设]`。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 中无任何假设（全是事实） | 输出"风险极低"评估，但仍按流程尝试从全局约束中挖掘风险 | 标注"基于事实链的风险推断，假设链为空" |
| 所有风险归类为 Paper Tiger | 提示"需增加外部视角——是否有未考虑的场景？" | 不阻塞，但必须在摘要中标注 Paper Tiger 占比 100% |
| 行动计划不可执行（无负责人、无日期） | 使用"待分配 / 待确认"占位 | 不阻塞，汇总待分配项到摘要 |
| PMContext 中 `[冲突]` 项涉及核心规则 | 风险章节单列冲突升级为 Tiger，不强行选定方向 | 在行动计划标注"需 PM 先解决冲突" |
| 假设清单置信度全 ≥ 8（低风险） | 标注"假设链置信度高，Tiger 升级概率低"，仍完成交叉检查 | 不阻塞，但摘要中标注"低风险场景" |
| Tiger 数量 > 5（行动计划过载） | 按紧急度排序，只保留 Top 5 Launch-Blocking，其余降级为 Fast-Follow | 不阻塞，但必须在摘要中说明降级 |
| 风险追溯失败（无法对应 PMContext 项） | 标 `[假设]` 并附推断依据 | 不阻塞，记入信息缺口清单 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 脱离 PMContext 凭空列风险 | 风险无追溯，与产品上下文脱节 |
| 把每个最小风险都升为 Tiger | Tiger 过多降低行动计划的可用性 |
| 行动计划不写负责人 | 无负责人=无人执行，premortem 失去意义 |
| 跳过假设清单交叉检查 | PMContext 中低置信度假设是最可能出问题的地方 |
| 不输出摘要直接结束 | PM 不知道要关注哪类风险 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"经过分析得到" | 空话，必须写明是同义词推导/多对多实体映射/边界隔离分析之一（ADR 0008 §11） |

## 产出示例

`/pm-premortem 会员体系重构` 产出摘要：

```
# Pre-Mortem: 会员体系重构

### 🐯 Tigers (真实风险)
| 风险 | 紧急度 | 缓解措施 | 负责人 | 截止 |
|------|--------|---------|--------|------|
| 年付定价不合理导致 LTV 下降 | Launch-Blocking | 做价格敏感度 A/B 测试 | PM | 上线前 2 周 |
| 续费提醒 push 被 iOS 屏蔽 | Fast-Follow | 备选短信通道 | 后端 | 上线后 7 天 |
| 订单表迁移导致历史数据丢失 | Launch-Blocking | 数据备份 + 回滚方案 | 后端 | 上线前 |

### 🦍 Elephants (未被讨论)
- 团队反映"年付退款政策还没定"——需在定价确认前敲定退款策略

### 假设交叉检查
- [假设: 用户续费率下降 12% 与定价有关，7/10] → 升级为 Tiger
```

### Further Reading

- [How Meta and Instagram Use Pre-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/risk-analysis-example.md](references/risk-analysis-example.md)（Tiger/Paper Tiger/Elephant 三分示例与行动计划模板）。

### 实战提示

- **Tiger 不超过 5 个**：再多行动计划不可执行。按紧急度排序，超出的降级为 Fast-Follow
- **假设交叉检查是核心**：PMContext 中置信度 ≤ 5 的假设，最可能升级为 Tiger，优先处理
- **Paper Tiger 也要有解释**："这是个假问题，因为…"——光说"不担心"不解决问题
- **Pre-Mortem 不是走形式**：如果所有风险都是 Paper Tiger，说明你没认真想失败
