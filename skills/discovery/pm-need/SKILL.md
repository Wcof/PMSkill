---
name: pm-need
description: 从模糊想法或用户诉求出发，全自动收集材料并推断澄清，沉淀成 PMContext。Use when starting from a vague idea or user request, or the user mentions 需求发现、collect needs、discovery.
disable-model-invocation: true
---

# /pm-need

> 你是一位资深产品经理。面对一个模糊想法或用户诉求，你需要快速将其转化为结构化的产品上下文（PMContext），让团队有据可依。本 skill 自动完成这件事。

全自动主入口：collect → refine → audit 一气呵成。支持两种模式：

- **正常模式**：产出 PMContext 后停在审计门，等 PM 确认后才进入 PRD/草图
- **零确认模式**（`--auto`）：一气呵成走完 collect → refine → PRD → 原型，不等待

## Purpose

全自动主入口：collect → refine → audit 一气呵成。PM 的唯一干预点是审计门——能扫到的绝不问、能推断的绝不等。

## Context

PM 面对模糊想法或用户诉求，需要快速转化为结构化产品上下文。本 skill 自动完成收集、推断、沉淀三步。

## Instructions

```
/pm-need <需求描述>                    → 正常模式：collect → refine → 🛑 审计门
/pm-need <需求描述> --auto             → 零确认模式：collect → refine → PRD → 原型，不暂停
/pm-need --collect-only                → 只收集，不精炼（debug 用）
/pm-need --refine-only                 → 只精炼，不收集（已有材料时用）
/pm-need --incremental                 → 增量更新已有 PMContext
```

`$ARGUMENTS` 为 PM 的需求描述，可包含：
- 一句话需求（如"我需要做个大屏"）
- URL 引用（如"相关上下文请参考 https://..."）— Agent 会自动抓取
- 多个 URL 用空格或逗号分隔

示例：
```
/pm-need 我需要做个数据大屏，相关上下文请参考 https://docs.example.com/dashboard-spec
/pm-need 会员体系重构，竞品参考 https://a.com https://b.com
/pm-need 会员体系重构 --auto          # 零确认模式
```

## 流程

### 1. Run `/pm-collect`

以 `$ARGUMENTS` 为种子，从四个来源自动扫描：
1. **URL 抓取** — 提取 `$ARGUMENTS` 中所有 URL，逐个抓取网页/文档内容。抓取失败标 `[待确认]`，不阻塞。
2. **对话上下文** — PM 在当前对话中说/粘贴的内容
3. **项目深扫描** — 主动扫描：
   - `README.md`、`CONTEXT.md`、`AGENTS.md`、`CLAUDE.md`、`.atomcode.md` 等根级配置
   - `docs/` 目录全部文件（设计文档、API 文档、用户手册、历史 PRD）
   - 近期 git commit messages（最近 30 条）
   - Issue / PR 标题和描述（若可访问）
   - 源代码中 `@todo`、`TODO:`、`FIXME:` 标记
   - 关键配置文件和入口文件（package.json、docker-compose.yml、main.ts 等）
   - 项目源文件的目录结构和命名模式
4. **知识库搜索** — 若配置了知识库路径，搜索相关文档

✅ **全自动**，无需 PM 介入。

### 2. Run `/pm-refine`

对收集到的材料自主推断澄清：
- 材料中有明确依据 → 写为**事实**，标注来源
- 可合理推断 → 写为**推断**，标 `[假设]` 附置信度(1-10)
- 材料完全缺失 → 标 `[待确认]`，记入信息缺口
- 不同材料矛盾 → 标 `[冲突]`，Agent 选更可信来源

8 个推断维度全覆盖：用户场景、边界条件、优先级、冲突检测、术语澄清、现状平替与摩擦力、技术与资源约束、价值验证度量。

✅ **全自动**，无需 PM 逐个确认。

### 3. 审计门（仅正常模式）

PMContext 落盘后，输出审计摘要：

```markdown
## 审计摘要

**PMContext 已落盘：** `docs/pm-context/pm-context.md`

### 置信度分布
| 类别 | 数量 | 占比 |
|------|------|------|
| 事实（有来源） | N | X% |
| [假设]（Agent 推断） | N | X% |
| [待确认]（材料不足） | N | X% |
| [冲突]（材料矛盾） | N | X% |

### 信息缺口（需 PM 补充）
- <维度>：<缺什么，建议 PM 提供什么>

### 项目扫描发现的材料
- 根级配置文件：N 个
- docs/ 文档：N 个
- 代码中的 TODO/FIXME：N 处
- git commits 扫描：最近 N 条
- 知识库引用：N 个（如配置）

### 下一步
- **通过审计** → 调用 `/pm-prd` 生成 PRD
- **零确认模式** → 自动进入 `/pm-prd --auto` → `/pm-sketch --prototype --auto`
- **补充材料** → 提供新材料后重新调用 `/pm-need`（增量更新）
- **修改 PMContext** → 直接编辑 `pm-context.md`，然后调用 `/pm-prd`
```

**🔴 CHECKPOINT · 🛑 STOP** — 正常模式下此审计门等待 PM 确认后进入 PRD/草图阶段。

### 4. 零确认模式（--auto）

`--auto` 模式下，审计门**不等待**：
1. 输出简短审计摘要（1-2 行）
2. 自动调用 `/pm-prd --auto` 生成 PRD
3. 自动调用 `/pm-sketch --prototype --auto` 生成全部草图 + HTML 原型
4. 最终输出一站式报告：

```markdown
## PMSkill 自动完成报告

### 链路用时
- collect: X 个来源，Y 个材料
- refine: Z 个推断维度
- PRD: ai-prd.md + human-prd.md
- 原型: prototype.html + 4 个 Mermaid 草图

### 产出物
- 📄 PMContext: docs/pm-context/pm-context.md
- 📄 AI PRD: docs/pm-context/prd/ai-prd.md
- 📄 Human PRD: docs/pm-context/prd/human-prd.md
- 🎨 HTML 原型: docs/pm-context/sketch/prototype.html
- 📊 Mermaid 草图: sketch/\*.md (wireframe/ia/state/flow)

### 置信度
- 事实: X%
- [假设]: X%
- [待确认]: X%
- [冲突]: X%
```

PM 可直接查看 HTML 原型预览，也可事后审计 PMContext 和 PRD。

## 产出示例 · 延伸参考 · 实战提示

详见 [references/examples-and-tips.md](references/examples-and-tips.md)。

## 增量更新

若 `pm-context.md` 已存在，且未指定 `--incremental` 时：
- 先输出"PMContext 已存在，是否覆盖？覆盖将丢失历史推断"
- 若确认 → 全新走完全流程
- 若否 → 退出

`--incremental` 模式：collect 只扫描新增材料，refine 只推断新增部分，增量写入。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `--auto` 模式下 collect 失败 | 不暂停，记录失败项到一站式报告的"失败清单" | refine 用已有材料继续，标到信息缺口 |
| `--auto` 模式下 refine 失败 | 不暂停，输出"refine 失败: <原因>"，PMContext 用 collect 原材料兜底 | 不阻塞 PRD 生成，但 PRD 标注"基于未精炼材料" |
| `--auto` 模式下 pm-prd 失败 | 不暂停，记录失败项，继续尝试 pm-sketch | 已生成 PMContext 仍落盘 |
| `--auto` 模式下 pm-sketch 失败 | 不暂停，一站式报告中标注草图失败原因 | 已生成 PRD 仍落盘 |
| `--incremental` 模式但 PMContext 不存在 | 退化为全新创建模式，提示"PMContext 不存在，改为全新创建" | 不阻塞 |
| PMContext 已存在且未指定 `--incremental` | 先输出"PMContext 已存在，是否覆盖？覆盖将丢失历史推断" | 用户选否则退出；选是则全新走完流程 |
| `$ARGUMENTS` 为空且无 PMContext | **🔴 STOP**：输出"请提供需求描述: `/pm-need <需求>`" | 不阻塞，提示后退出 |
| `--collect-only` 和 `--refine-only` 同时使用 | **🔴 STOP**：输出"两个模式冲突，只能选一个" | 不阻塞，改为默认全流程 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 在 collect 和 refine 之间插入人工确认 | 破坏全自动体验，违背零确认设计 |
| 收集阶段直接提取事实改写原文 | 材料应原样整理，事实提取是 refine 的职责 |
| 原始材料不整理就堆给 refine | 材料过于零散，refine 维度推断不准 |
| 零确认模式不输出置信度分布 | PM 事后无法判断哪些区域需要复核 |
| 私用 URL 抓取失败静默跳过 | 关键材料缺失会导致 PMContext 质量下降 |
| 跳过源代码扫描 | 项目中可能已有技术约束、API 定义等关键信息 |
| `--auto` 模式遇子 skill 失败就全链路回滚 | 已生成部分仍落盘，失败项单独标注 |
