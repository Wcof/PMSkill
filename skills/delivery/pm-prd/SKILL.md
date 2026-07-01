---
name: pm-prd
description: 从 PMContext 生成 PRD 文档——给 AI 的可执行规则版和给人的评审叙事版两种形态。支持 --auto 零确认、--skip-ai / --skip-human 单形态输出。Use when generating PRD from PMContext, or the user mentions 生成PRD、prd、需求文档、产品规格、ai-prd、human-prd、双形态PRD.
disable-model-invocation: true
---

# /pm-prd

## Purpose

从 PMContext 生成两份 PRD——一份给 AI 直接执行（可执行规则+验收标准），一份给人评审决策（决策理由+自然叙事）。PRD 是 PMContext 的 View，同源同骨架，差异只在写法。

## Context

PMContext 已沉淀了事实/假设/冲突/待确认的结构化上下文。PRD 的职责是将这些转化为两种受众可用的形态。

## Instructions

### 1. 读取 PMContext

从 `docs/pm-context/pm-context.md` 读取。若不存在：
- 有 `$ARGUMENTS` → 调用 `/pm-need $ARGUMENTS`，完成后回到本流程
- 无 `$ARGUMENTS` → 🔴 STOP：输出"未找到 PMContext，先运行 `/pm-need <需求>`"

- [ ] PMContext 已读取且非空
- [ ] 概述/页面定义/全局约束/假设清单/风险项/信息缺口全部提取

### 2. 生成两种 PRD

Run `/pm-aiprd` — 生成 `docs/pm-context/prd/ai-prd.md`
Run `/pm-humanprd` — 生成 `docs/pm-context/prd/human-prd.md`

- [ ] ai-prd.md 已落盘
- [ ] human-prd.md 已落盘

### 3. 审计（仅非 --auto 模式）

展示摘要：ai-prd N 个用户故事 M 条规则 / human-prd N 条含决策理由 / 未覆盖风险项。

**🔴 CHECKPOINT** — 等用户确认。

- [ ] 审计摘要已输出
- [ ] 用户已确认（或 --auto 跳过）

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的编排职责：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（编排） | 编排 /pm-aiprd 和 /pm-humanprd 生成双形态 PRD，确保两种 PRD 同源同骨架 | 不回灌（产出 View） |

执行时依次调用 /pm-aiprd → /pm-humanprd。子 Skill 各自写入 `.loop/` 中间工件。
达阈值的关键信息自动回灌到 PMContext 对应 heading（不开新 heading、走现有标记体系）。

**产出约束**：
- ai-prd 和 human-prd 必须同源同骨架——同一条需求在两种 PRD 中表述不同但追溯的 PMContext 项相同
- 同源项出现分歧时以 PMContext 为准修正，标注修正项
- 必须产出**双形态 PRD 交付物清单**：ai-prd 含 N 个用户故事 + M 条可执行规则 + K 条验收标准；human-prd 含 N 条含决策理由规则 + 格式纪律检查结果
- [待确认] 占比 > 50% 时 ai-prd 标 🔴 不可执行、human-prd 只输出信息缺口清单

**依赖检查**：ai-prd 和 human-prd 的同源项是否一致？[待确认] 占比是否超阈值？

## 零确认模式（--auto）

当通过 `/pm-prd <需求描述>` 或 `/pm-need --auto` 调用时：
1. 自动 run `/pm-collect` + `/pm-refine` 生成 PMContext
2. 自动 run `/pm-aiprd` + `/pm-humanprd` 生成 PRD
3. 输出审计摘要后**不等待确认**，直接落盘完成
4. 输出摘要包含置信度分布 + 信息缺口，供 PM 事后审计

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 且无 `$ARGUMENTS` | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 不存在但有 `$ARGUMENTS` | 自动调用 `/pm-need $ARGUMENTS` 生成 PMContext，结束后回到 PRD 生成 | pm-need 失败则 STOP 并提示失败原因 |
| pm-aiprd 生成失败 | 单独输出 human-prd，标注 `ai-prd 生成失败: <原因>` | 不阻塞，提示用户单独重跑 `/pm-aiprd` |
| pm-humanprd 生成失败 | 单独输出 ai-prd，标注 `human-prd 生成失败: <原因>` | 不阻塞，提示用户单独重跑 `/pm-humanprd` |
| `--auto` 模式下任一子 skill 失败 | 不暂停，记录失败项到一站式报告的"失败清单"章节 | 其他子 skill 结果仍落盘 |
| `--skip-ai` 和 `--skip-human` 同时使用 | **🔴 STOP**：输出"两个 skip 标记冲突，至少生成一种 PRD" | 不阻塞，改为只生成 ai-prd |
| PMContext 中 `[冲突]` 项涉及核心规则 | PRD 中标注冲突项，不强行选定方向 | 在审计摘要中汇总冲突项供 PM 决策 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 跳过 PMContext 直接从聊天生成 PRD | PRD 无溯源，关键决策丢失 |
| 把 `[待确认]` 项写成确定性要求 | PM 误判为事实，导致交付偏差 |
| 在 ai-prd 中塞 narrative 而不给可执行规则 | Agent 无法直接执行，失去"给 AI"的意义 |
| 在 human-prd 中塞 Agent Context | 人类读者看不懂技术细节 |
| 自动模式不输出置信度分布 | PM 事后无法判断哪些部分需要复核 |
| `--auto` 模式遇到子 skill 失败就全链路回滚 | 其他成功部分仍落盘，失败项单独标注 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"经过分析得到" | 空话，必须写明是同义词推导/多对多实体映射/边界隔离分析之一（ADR 0008 §11） |

## 产出示例

`/pm-prd 会员体系重构` 产出两份文件：

| 产物 | 路径 | 内容概要 |
|------|------|---------|
| AI PRD | `prd/ai-prd.md` | 6 条可执行规则、4 个用户故事、7 条验收标准、Agent Context（技术栈/目录结构） |
| Human PRD | `prd/human-prd.md` | 决策理由表、"为什么现在做"背景、3 项 [待确认] 标注、追溯清单 |

### Further Reading

- [PM Compass 8-section PRD Template](https://www.productcompass.pm/p/prd-template)
- [AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [An Introduction to the Product Trio](https://www.productcompass.pm/p/product-trio)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/dual-form-example.md](references/dual-form-example.md)（双形态 PRD 同源骨架对比示例）。

### 实战提示

- **优先跑 `--auto`**：PMContext 不存在时自动链路远比手动快
- **审计摘要要读**：黑名单把 `[待确认]` 写成确定项是最高频错误
