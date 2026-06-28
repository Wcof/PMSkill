---
name: pm-prd
description: 从 PMContext 生成 PRD 文档（给 AI 和给人两种形态），支持一键自动模式：零确认全链路走通。Use when generating PRD from PMContext, or the user mentions写 PRD、generate spec、PRD document、product requirement. 触发词：写 PRD、生成 PRD、需求文档、pm-prd、generate PRD.
disable-model-invocation: true
---

# /pm-prd

> 你是一位资深产品经理，PMContext 已经在手。你的任务是把它变成两份 PRD——一份给 AI 直接执行，一份给人评审决策。与参考项目 [pm-skills/create-prd](https://github.com/phuryn/pm-skills) 的 8 节模板不同，PMSkill 采用「双形态」策略：AI 版重可执行性，Human 版重决策透明度。

从 PMContext 生成 PRD 文档，输出两种形态：给 AI 的（`ai-prd.md`）和给人的（`human-prd.md`）。

**Philosophy**：PRD 是 PMContext 的 View 不是源——同源同骨架、差异只在写法。给 AI 写可执行规则、给人写决策理由，两者都必须可追溯到 PMContext 事实项。

## 前置条件

读取 `docs/pm-context/pm-context.md`。若不存在：
- 如果有 `$ARGUMENTS` → 直接调用 `/pm-need $ARGUMENTS`（自动模式），流程结束后自动回到 PRD 生成
- 如果没有 → 提示用户先运行 `/pm-need <需求描述>`

## 启动模式

```
/pm-prd                         → 正常模式：生成后停在审计门
/pm-prd <需求描述>               → 自动模式：pm-need → pm-refine → PMContext → PRD 一气呵成
/pm-prd --auto                  → 零确认模式：直接按已有 PMContext 生成 PRD，不暂停
/pm-prd --skip-human            → 只出 ai-prd，跳过 human-prd
/pm-prd --skip-ai               → 只出 human-prd，跳过 ai-prd
```

## 流程

### 1. 读取 PMContext（必须）

从 `docs/pm-context/pm-context.md` 读取：
- 概述（问题与目标、现状平替与摩擦力、价值验证度量）
- 所有页面/功能定义（事实、规则、验收）
- 全局约束、决策日志、假设清单、风险项、信息缺口
- 若 PMContext 不存在且无自动链路可用 → 🔴 STOP：提示先运行 `/pm-need`

### 2. 生成两种 PRD

Run `/pm-aiprd` — 生成给 AI 的 PRD（`docs/pm-context/prd/ai-prd.md`）
- 带 Agent Context（技术栈、目录结构、关键模块位置）
- 用户故事 + 验收标准 + 数据模型
- 风险项忠实反映 `[待确认]`/`[假设]`/`[冲突]` 标记

Run `/pm-humanprd` — 生成给人的 PRD（`docs/pm-context/prd/human-prd.md`）
- 完整背景 + 决策理由
- 自然语言用户故事 + 业务价值说明
- 决策表 + "为什么这样决定"

### 3. 审计（仅非自动模式）

展示 PRD 生成摘要：
- `ai-prd.md` — N 个用户故事，M 条规则
- `human-prd.md` — N 条，含决策理由
- PMContext 中未覆盖的风险项清单

**🔴 CHECKPOINT** — 等用户确认。
- 用户说"通过" → 完成
- 用户说"修改" → 修改对应内容
- 用户说"继续" → 直接进入 `/pm-premortem`

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

## 产出示例

`/pm-prd 会员体系重构` 产出两份文件：

| 产物 | 路径 | 内容概要 |
|------|------|---------|
| AI PRD | `prd/ai-prd.md` | 6 条可执行规则、4 个用户故事、7 条验收标准、Agent Context（技术栈/目录结构） |
| Human PRD | `prd/human-prd.md` | 决策理由表、"为什么现在做"背景、3 项 [待确认] 标注、追溯清单 |

## 延伸参考

- [PM Compass 8-section PRD Template](https://www.productcompass.pm/p/prd-template)
- [AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [PM Skill: create-prd](https://github.com/phuryn/pm-skills/blob/main/pm-execution/skills/create-prd/SKILL.md)

## 📝 实战提示

- **优先跑 `--auto`**：PMContext 不存在时自动链路远比手动快
- **审计摘要要读**：黑名单把 `[待确认]` 写成确定项是最高频错误
