---
name: pm-premortem
description: 从 PMContext 出发假设失败并倒推风险，产出 Tiger/Paper Tiger/Elephant 三类风险 + 紧急度分级 + 行动计划。Use when preparing for launch, stress-testing a product plan, or identifying what could go wrong. 触发词：Pre-Mortem、风险分析、假设失败、stress test plan、风险倒推、pm-premortem.
---

# /pm-premortem

> 你是一位资深产品经理，正在为一个即将上线的产品做 Pre-Mortem。方法论源自 [PM Compass 的 Pre-Mortem 实践](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)（Meta/Instagram 团队使用）：**假设上线失败，然后倒推为什么**。

从 PMContext 出发，假设产品上线失败，倒推风险并分类，产出行动计划。PMContext 的风险分析 View，和 PRD/草图平级。

**Philosophy**：Pre-Mortem 不是列全部风险而是筛可行动风险——Tiger 必须有负责人和日期、Paper Tiger 必须说明为何不是真风险、Elephant 必须说明为何暂不处理。假设清单交叉检查是核心机制，低置信度假设最可能升级为 Tiger。

## 前置条件

读取 `docs/pm-context/pm-context.md`。若不存在，提示先运行 `/pm-need`。

## 流程

### 1. 读取 PMContext

理解产品目标、用户场景、规则、验收标准、全局约束、假设清单、风险项。

### 2. 假设失败

想象产品上线 14 天后失败了——用户不采用、指标没达标、出了事故。问自己：
- 什么出了错？
- 我们遗漏了什么？
- 我们对什么过度自信了？

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

## 产物

写入 `docs/pm-context/premortem.md`，结构：

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
| 风险 | 建议调查方式 |
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
| 所有风险归类为 Paper Tiger | 提示"建议增加外部视角——是否有未考虑的场景？" | 不阻塞，但必须在摘要中标注 Paper Tiger 占比 100% |
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

## 延伸参考

- [How Meta and Instagram Use Pre-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [PM Compass Pre-Mortem Template](https://github.com/phuryn/pm-skills/blob/main/pm-execution/skills/pre-mortem/SKILL.md)
