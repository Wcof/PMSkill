---
name: pm-setup
description: 首次使用 PMSkill 时配置项目（产物目录/语言/知识库路径/Agent 规则）。Use when first configuring PMSkill, or the user mentions 初始化、setup PM config.
disable-model-invocation: true
---

# /pm-setup

> 你是一位产品技术布道师，需要在当前项目中首次配置 PMSkill 环境。你的任务不是手动配，而是**探索 → 询问 → 写入**，让后续 Skill 自动读到配置。

首次使用 PMSkill 时配置项目。运行一次即可，后续 Skill（`/pm-need`、`/pm-prd`、`/pm-sketch`）自动读取配置。

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Purpose

首次使用 PMSkill 时配置项目。运行一次即可，后续 Skill 自动读取配置。配置是项目契约——只写一次、所有下游 skill 共享。

## Context

项目可能已有 CLAUDE.md/AGENTS.md，可能已有 docs/pm-context/。本 skill 探索项目现状，逐一确认配置项，写入 Agent 规则文件。

## Instructions

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a git repo? Remote host?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already a `## PMSkill` section in either?
- `CONTEXT.md` at the repo root — does it exist? (PMSkill treats it as the domain glossary source)
- `docs/pm-context/` — does this skill's prior output already exist?
- 当前 Agent 类型 — Claude Code / Codex / Trae（从会话环境推断，不直接问用户）

### 2. Present findings and ask

Summarise what's present and what's missing. Then walk the user through the three decisions **one at a time** — present a section, get the user's answer, then move to the next. Don't dump all three at once.

Assume the user does not know what these terms mean. Each section starts with a short explainer (what it is, why PMSkill needs it, what changes if they pick differently). Then show the choices and the default.

**Section A — 产物目录.**

> Explainer: PMSkill 把所有产出（PMContext、PRD、草图）落盘成 markdown 文件，下游 Skill 读这些文件而不是靠对话记忆。产物目录就是这些文件的家。默认放在 `docs/pm-context/` 下，贴近大多数项目的文档习惯；你也可以指定别的位置（比如 repo 根目录、或 `docs/pm/`）。

Default: `docs/pm-context/`. 若用户自定义，记录其路径。目录内约定：

- `pm-context.md` — PMContext（唯一 Entity，源）
- `prd/ai-prd.md` / `prd/human-prd.md` — 给 AI / 给人的 PRD（下游 View）
- `sketch/wireframe.md` / `sketch/ia.md` / `sketch/state.md` / `sketch/flow.md` — 草图（下游 View）
- `collect/` — `/pm-collect` 整理后的材料（按类型聚合为单 md）

**Section B — 语言偏好.**

> Explainer: PMSkill 产出的 PMContext 和 PRD 用什么语言写。中文适合国内团队评审；英文适合开源或跨国协作；双语会同时产出两份（成本更高，仅在需要对外发布时选）。

Choices:

- **中文**（default）
- **英文**
- **双语** — 每个产物产出中英两份

**Section C — 知识库路径.**

> Explainer: PMSkill 的 `/pm-collect` 除了扫描当前项目，还会从你指定的知识库中提取材料。知识库是项目外部的文档集合（竞品分析、用户调研、行业报告、历史 PRD 等），`/pm-collect` 会按需搜索其中与当前需求相关的内容。如果不指定，collect 只扫描当前项目。

Choices:

- **跳过**（不配置知识库，collect 仅扫描当前项目）
- **一个或多个路径** — 本地目录路径，用逗号分隔。如：`~/docs/pm-kb, ~/docs/competitor-research`

Default: 跳过。若用户指定路径，验证路径存在后再记录。

**Section D — Agent 规则落点.**

> Explainer: PMSkill 需要在项目的 Agent 指令文件里写一小段规则，告诉后续 Agent "PMContext 是唯一源、下游 View 都从它读、风险用显式标记"。规则只写一次，所有 PMSkill 命令共享。落在 `CLAUDE.md` 还是 `AGENTS.md` 取决于你用哪个 Agent。

Default posture: 若 `CLAUDE.md` 存在，写入它；否则若 `AGENTS.md` 存在，写入它；若都不存在，问用户要创建哪个 —— 不要替用户决定。Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

**冲突处理（扩展）**：若 `CLAUDE.md` 和 `AGENTS.md` 同时存在：
1. 检测当前 Agent 类型（从会话环境推断：Claude Code → CLAUDE.md，Codex → AGENTS.md 等）
2. 若无法推断，问用户要用哪个
3. 只编辑被选中的那个，不要同时编辑两个文件

### 3. Confirm and edit

Show the user a draft of:

- The `## PMSkill` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The `docs/pm-context/` directory layout

Let them edit before writing.

**🔴 CHECKPOINT** — Confirm with user before writing to disk.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

If a `## PMSkill` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## PMSkill

- 领域术语：见 CONTEXT.md（若不存在，由 /pm-need 在首次澄清时沉淀）
- 产物目录：docs/pm-context/
- PMContext（唯一 Entity）：docs/pm-context/pm-context.md
- 下游 View：PRD（`prd/ai-prd.md` / `prd/human-prd.md`）、草图（`sketch/*.md`）均从 PMContext 派生
- 风险标记：[待确认] / [假设] / [冲突] 写在正文里，无需独立检查报告
- 知识库：<用户指定路径，或"无">
- 无 hook：/pm-collect 从对话上下文 + 项目扫描 + 知识库搜索收集，不拦截 Agent 会话
- 语言：<用户选择>
```

Then create the产物目录（若不存在）：

- `docs/pm-context/` — 空目录即可，`/pm-need` 首次运行时创建 `pm-context.md`

### 5. Done

Tell the user setup is complete and which PMSkill commands will now read from this config:

- `/pm-need` → 写入 `docs/pm-context/pm-context.md`
- `/pm-prd` → 从 PMContext 生成 `prd/ai-prd.md` / `prd/human-prd.md`
- `/pm-sketch` → 从 PMContext 生成 `sketch/*.md`（wireframe/ia/state/flow）+ HTML 原型（`--prototype`）
- 零确认模式：`/pm-need <需求描述> --auto` 可一键全自动完成收集 → PMContext → PRD → 原型

Mention they can edit the `## PMSkill` block directly later — re-running `/pm-setup` is only necessary if they want to switch产物目录、改语言、或换 Agent 规则落点。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 非 git 仓库（`git remote -v` 失败） | 跳过 git 元数据收集，提示"PMSkill 在非 git 仓库中运行，部分扫描能力受限" | 不阻塞，继续配置 |
| `CLAUDE.md` 和 `AGENTS.md` 同时存在 | 检测当前 Agent 类型推断落点；无法推断则问用户 | 只编辑被选中的那个，绝不同时编辑两个 |
| `CLAUDE.md`/`AGENTS.md` 已含 `## PMSkill` 块 | 原位更新内容，不追加重复块 | 不覆盖用户对其他章节的编辑 |
| 用户指定知识库路径不存在 | 当场提示"路径不存在"，要求重新输入或跳过 | 不写入错误路径，跳过知识库配置 |
| 用户指定产物目录在 gitignore 中（如 `docs/`） | 明示"该目录会被 git 局蔽，PMSkill 产物不会进版本库" | 问用户接受现状 / 改路径 / 改 gitignore 三选一 |
| 产物目录已存在且含旧 PMContext | 不覆盖，提示"已有 PMSkill 产物，是否复用？" | 复用则跳过目录创建；不复用则备份后重建 |
| Agent 类型无法从会话环境推断 | 问用户当前 Agent 类型（Claude Code/Codex/Trae） | 不臆造，落点改为问用户选择 CLAUDE.md 或 AGENTS.md |
| 用户中途放弃（连续 3 次无回应） | 保存已收集配置到 `.pmskill-setup.tmp`，提示"可下次 `/pm-setup --resume` 继续" | 不写入部分配置到 Agent 文件 |

## 产出示例 · 延伸参考 · 实战提示

详见 [references/examples-and-tips.md](references/examples-and-tips.md)。

| 反模式 | 为什么不要做 |
|--------|------------|
| 替用户决定创建 `CLAUDE.md` 还是 `AGENTS.md` | 不同 Agent 绑定不同文件名，替用户决定可能导致后续 Skill 无法读取配置 |
| 两个 Agent 文件同时写入 | 只编辑被选中的那个；两个文件都写会导致配置冲突 |
| 重复注册 PMSkill 块 | 若 `## PMSkill` 已存在，覆盖更新而非追加 |
| 预判模板偏好 | pm-setup 只配置目录/语言/知识库路径，不配置 PRD 或 PMContext 的模板细节 |
| 注册 hook | `/pm-collect` 从对话上下文 + 项目扫描 + 知识库搜索收集，不需要拦截 Agent 会话 |
| 忽略项目扫描已存在的配置 | 先检查 `CLAUDE.md`/`AGENTS.md`/`.atomcode.md` 中是否已有 PMSkill 块，有则直接复用 |
