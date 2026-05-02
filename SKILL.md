---
name: prd-helper
description: Use this skill when transforming product discussions, meeting notes, prototype notes, customer feedback, review notes, or agent session summaries into structured PRD documents through collect, refine, relate, and generate steps.
---

# PRD Helper Skill

你正在帮助用户处理产品需求上下文（product requirement context）。

不要直接从原始材料生成最终 PRD，必须走完整流程。

在项目中使用前，先安装完整的 `prd-helper` Skill。

默认 Step 0 安装：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

在安装器（installer）中选择 `prd-helper`，再选择要安装到哪些编码 Agent（coding agents）。使用方向键移动，使用 Space 勾选，使用 Enter 确认，不依赖数字输入。

安装完成后，在 Agent 中运行初始化：

```text
/prd-setup
```

Agent 应询问并确认：

- PRD Helper 文档保存目录，默认 `docs/prd-helper/`。
- 当前项目启用哪些 Agent：Codex、Claude Code、Trae 或 Trae CN。
- 主动采集是否必须显式开启，默认只通过 `/prd-start` 开启。

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
| `/prd-setup` | 初始化当前项目：询问配置、创建 docs 根目录、写入配置、准备采集目录。 |
| `/prd-start` | 开启 PRD 采集会话。创建 `collect-state.md`、`active/`、`passive/`、`source-index.md`，并设置 `capture_mode: on`。 |
| `/prd-pause` | 暂停当前采集会话，设置 `capture_mode: paused`，停止写入会话轮次。 |
| `/prd-resume` | 恢复当前采集会话，设置 `capture_mode: on`。 |
| `/prd-stop` | 停止当前采集会话，设置 `capture_mode: off`，生成 `collect-summary.md` 和 `check.md`。 |
| `/prd-status` | 从 `collect-state.md` 查看当前采集状态。 |
| `/prd-remove` | 从当前项目卸载 PRD Helper：先清理 Agent 配置块，再卸载 Skill。 |
| `/remove prd-helper` | `/prd-remove` 的别名，用于支持参数式斜杠命令的平台。 |

当 `capture_mode == on` 时，通过以下脚本把每轮对话完整记录为 `User Query + Agent Answer`：

```bash
python3 scripts/capture-source.py --agent <name> --user-query-file <path> --agent-answer-file <path>
```

被动材料直接放入 `docs/prd-helper/01-collect/passive/`，然后扫描：

```bash
python3 scripts/scan-passive.py --root docs/prd-helper/01-collect
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
/prd-setup
```

当用户发送 `/prd-setup` 时，先询问上述初始化问题，然后执行已安装 Skill 目录中的 setup 脚本。按顺序尝试以下路径，使用第一个存在的路径：

```bash
python3 .agents/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
python3 .claude/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
python3 .trae/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
```

从项目中卸载此 Skill：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

交互式选择卸载：

```bash
npx skills@latest remove
```

卸载 Skill 不会删除 `docs/prd-helper/` 中已经生成的项目文档。

配置清理命令会删除 `AGENTS.md`、`CLAUDE.md` 和 Trae `project_rules.md` 中的 PRD Helper 标记块；`skills remove` 会删除已安装的 Skill 目录。

当用户发送 `/prd-remove` 或 `/remove prd-helper` 时，运行已安装 Skill 目录中的卸载脚本。除非当前 Agent 无法执行命令，否则不要要求用户手动运行 shell 命令。

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
