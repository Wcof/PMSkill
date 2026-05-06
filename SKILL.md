---
name: prd-helper
description: 用于把产品讨论、会议纪要、原型说明、客户反馈、评审记录或 Agent 会话摘要，通过采集、精炼、关联、生成四步转成结构化 PRD 文档。Use this skill to transform product context into structured PRD docs.
allowed-tools: Bash
---

# PRD Helper Skill

你正在帮助用户处理产品需求上下文（product requirement context）。

不要直接从原始材料生成最终 PRD，必须走完整流程。

## Language Rule

安装器（installer）本身可能显示英文，但 Skill 安装完成后，Agent 必须根据用户语言选择输出语言：

- 如果用户主要使用中文，默认使用中文，并在关键术语后保留英文括注，例如“采集（Collect）”。
- 如果用户主要使用英文，默认使用英文，并在第一次出现关键模块时保留中文括注。
- 如果用户中英混合，使用中英双语关键字段，正文跟随用户主要语言。
- 如果无法判断用户偏好，在第一次响应时询问：`请选择语言 / Choose language: 中文 or English`。
- `/prd-helper`、`/prd-start`、`/prd-grill`、`/prd-status`、`/prd-remove` 的提示必须跟随上述语言策略。

在项目中使用前，先安装完整的 `prd-helper` Skill。

## Activation Rule

当用户触发 `/prd-helper` 时，必须直接执行初始化脚本。初始化脚本是幂等的：已存在的 docs 产物会保留，缺失的 Agent 配置和 Claude Code 斜杠命令会被补齐。不要只根据 `docs/prd-helper/prd-helper-config.md` 存在就判断完成，也不要只提示用户再去运行别的命令。

初始化判定：

- 如果 `docs/prd-helper/prd-helper-config.md` 不存在，视为未初始化。
- 如果当前项目缺少 `CLAUDE.md` 或 `AGENTS.md` 中的 PRD Helper 配置块，也应补写配置块。
- 如果当前 Agent 是 Claude Code，还必须创建 `.claude/commands/prd-start.md`、`.claude/commands/prd-status.md` 等命令文件，让 `/prd-start` 成为真实可见的斜杠命令。
- 如果当前 Agent 是 Claude Code，`/prd-start` 与 `/prd-resume` 必须写入 `.claude/settings.json` 中的 `UserPromptSubmit` 与 `Stop` hooks，让会话轮次自动落盘；`/prd-pause` 与 `/prd-stop` 必须清理这些 hooks。
- 如果 docs 配置已存在但 `.claude/commands/prd-start.md` 不存在，视为半初始化，必须重新执行 setup 修复。

默认自动初始化命令：

```bash
python3 .agents/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .claude/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .trae/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
```

按顺序尝试以上路径，使用第一个存在的脚本。如果三个路径都不存在（安装不完整），执行以下自修复命令后重试：

```bash
npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y
```

自修复后再次按顺序尝试上述三个路径。当前 Agent 是 Claude Code 时，必须带上 `--agent claude-code`，确保生成 `.claude/commands/prd-start.md` 等命令文件。初始化完成后，告诉用户下一步发送 `/prd-start` 开启采集；如果命令刚生成但 Claude Code 命令列表未刷新，提示用户开启新会话后再输入 `/prd-start`。

默认 Step 0 安装：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

在安装器（installer）中选择 `prd-helper`，再选择要安装到哪些编码 Agent（coding agents）。使用方向键移动，使用 Space 勾选，使用 Enter 确认，不依赖数字输入。

安装完成后，在 Agent 中运行初始化命令：

```text
/prd-helper
```

Agent 应自动初始化当前项目，默认使用 `docs/prd-helper/`、启用已安装 Agent，并设置采集策略为只通过 `/prd-start` 显式开启。初始化完成后，Claude Code 项目会生成 `/prd-start`、`/prd-pause`、`/prd-resume`、`/prd-stop`、`/prd-status`、`/prd-remove`。

通过斜杠命令从当前项目卸载：

```text
/prd-remove
```

Agent 必须执行已安装 Skill 目录中的卸载脚本。按顺序尝试以下路径，使用第一个存在的路径：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .trae/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

如果三个路径都不存在，先执行 `npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y` 自修复，再重试。

卸载全局安装（global scope）：

```bash
npx skills@latest remove prd-helper --agent '*' --global -y
```

始终遵循以下产品工作流：

0. 安装完整 Skill（Install）
1. 采集（Collect）
2. 精炼（Refine）
3. 关联（Relate）
4. 生成（Generate）

每一步完成后都必须检查。

## Core Rule

四个业务模块是：

- collect
- refine
- relate
- generate

检查（Check）是贯穿所有模块的质量门禁，不是第五个业务模块。

## 指令（Commands）

采集模块通过显式指令支持主动采集：

| Command | Action |
|---------|--------|
| `/prd-helper` | 初始化当前项目：创建 docs 根目录、写入配置、准备采集目录、生成后续命令文件。 |
| `/prd-start` | 开启 PRD 采集会话。创建 `collect-state.md`、`active/`、`passive/`、`source-index.md`，设置 `capture_mode: on`，并启用 Claude Code hooks 自动采集后续完整会话轮次。 |
| `/prd-pause` | 暂停当前采集会话，设置 `capture_mode: paused`，清理 Claude Code hooks，停止写入会话轮次。 |
| `/prd-resume` | 恢复当前采集会话，设置 `capture_mode: on`，重新启用 Claude Code hooks。 |
| `/prd-stop` | 停止当前采集会话，设置 `capture_mode: off`，清理 Claude Code hooks，生成 `collect-summary.md` 和 `check.md`。 |
| `/prd-status` | 从 `collect-state.md` 查看当前采集状态。 |
| `/prd-grill` | 开启 Grill 战斗模式：扫描已采集材料找矛盾，持续压力测试产品方案，实时更新 CONTEXT.md，按需创建 ADR。需先 `/prd-start`。 |
| `/prd-remove` | 从当前项目卸载 PRD Helper：先清理 Agent 配置块，再卸载 Skill。 |

当 `capture_mode == on` 时，Claude Code 通过项目级 hooks 自动把每轮对话完整记录为 `User Query + Agent Answer`。手动补录或其他 Agent 可直接调用同一个写入脚本：

```bash
python3 modules/collect/scripts/capture-source.py --agent <name> --user-query-file <path> --agent-answer-file <path>
```

被动材料直接放入 `docs/prd-helper/01-collect/passive/`，然后扫描：

```bash
python3 modules/collect/scripts/scan-passive.py --root docs/prd-helper/01-collect
```

## Workflow

### Step 0：安装（Install）

安装完整 `prd-helper` Skill。不要把 collect、refine、relate、generate 拆成独立 Skill 安装。

默认安装：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

交互式安装：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

交互安装时，使用方向键移动，Space 勾选，Enter 确认。

安装后运行：

```text
/prd-helper
```

当用户发送 `/prd-helper` 时，自动执行已安装 Skill 目录中的 setup 脚本。setup 是幂等修复入口，不要因为 `docs/prd-helper/prd-helper-config.md` 已存在而跳过。按顺序尝试以下路径，使用第一个存在的路径：

```bash
python3 .agents/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .claude/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .trae/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
```

如果三个路径都不存在（安装不完整），先执行 `npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y` 自修复，再重试。

如果用户明确要求自定义 docs 目录或 Agent 范围，再询问配置项。

从项目中卸载此 Skill：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .trae/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

如果三个路径都不存在，先执行 `npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y` 自修复，再重试。

交互式选择卸载：

```bash
npx skills@latest remove
```

卸载 Skill 不会删除 `docs/prd-helper/` 中已经生成的项目文档。

配置清理命令会删除 `AGENTS.md`、`CLAUDE.md` 和 Trae `project_rules.md` 中的 PRD Helper 标记块；`skills remove` 会删除已安装的 Skill 目录。

当用户发送 `/prd-remove` 时，运行已安装 Skill 目录中的卸载脚本。除非当前 Agent 无法执行命令，否则不要要求用户手动运行 shell 命令。

### Step 1: Collect

Read `modules/collect/guide.md` and use templates in `modules/collect/templates/`.

Save raw input to `docs/prd-helper/01-collect/`.

After collecting, run collect check and output `01-collect/check.md`.

### Step 2: Refine

Read `modules/refine/guide.md` and use templates in `modules/refine/templates/`.

Extract structured information to `docs/prd-helper/02-refine/`.

After refining, run refine check and output `02-refine/check.md`.

### Step 3: Relate

Read `modules/relate/guide.md` and use templates in `modules/relate/templates/`.

Build relations in `docs/prd-helper/03-relate/`.

After relating, run relate check and output `03-relate/check.md`.

### Step 4: Generate

Read `modules/generate/guide.md` and use templates in `modules/generate/templates/`.

Generate structured documents in `docs/prd-helper/04-generate/`.

After generating, run generate check and output `04-generate/check.md`.

### Final Check

Read `checks/guide.md` and use templates in `checks/templates/`.

Final check output goes to `docs/prd-helper/05-check/`, including `context-delta.md`.
