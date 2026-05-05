# PRD Helper

![PRD Helper Skill Kit overview](support/assets/prd-helper-project-overview.svg)

## 一句话讲通

PRD Helper 是一个可安装的单体 Agent Skill，把产品讨论、会议纪要、客户反馈、旧文档和 Agent 会话，按“采集 Collect → 精炼 Refine → 关联 Relate → 生成 Generate → 检查 Check”的流程，变成可追溯、可审计、可交给 Agent 和人类继续使用的 PRD 上下文。

## 项目介绍

PRD Helper 不是四个分散的小工具，也不是直接把聊天记录丢给 AI 生成 PRD。它的核心是一个根入口 `SKILL.md`，下面显式拆成四个业务模块：

| 模块 | 做什么 | 关键产物 |
|------|--------|----------|
| Collect 采集 | 保存原始材料，支持主动会话采集和被动文件投放，只做索引、摘要和轻量噪音标记 | `01-collect/`、`source-index.md`、`collect-state.md` |
| Refine 精炼 | 按用户故事（US）组织事实、决策、约束、目标、冲突、问题和 AI 推断 | `02-refine/index.md`、`US-*/` |
| Relate 关联 | 把 US 和实体织成关系网络，沉淀主题、决策链路和概念层级 | `03-relate/relations.md`、`themes.md`、`context-map.md` |
| Generate 生成 | 基于精炼与关联结果生成 Agent 维度和人类维度 PRD | `04-generate/agent/`、`04-generate/human/` |

`checks/` 不是第五个业务模块，而是横向质量门禁。每个阶段都要产出 `check.md`，最终通过 `/prd-check` 汇总到 `05-check/final-check.md`。

当前项目的关键能力：

| 能力 | 当前实现 |
|------|----------|
| Skill 安装 | `npx skills@latest add Wcof/PRDContextEngine`，安装器只会发现一个 Skill：`prd-helper` |
| 项目初始化 | `/prd-helper` 幂等初始化项目，创建目录、配置 Agent、生成后续命令 |
| Claude Code 采集 | 生成 `.claude/commands/prd-*.md`，`/prd-start` 和 `/prd-resume` 写入 Hook，`/prd-pause` 和 `/prd-stop` 清理 Hook |
| Codex 采集 | 安装 `~/.codex/plugins/prd-helper/` 插件，结合 `AGENTS.md` 指令和 JSONL 会话扫描兜底 |
| 被动材料 | 人工把会议纪要、旧 PRD、客户反馈等放入 `docs/prd-helper/01-collect/passive/` |
| 生成模式 | `/prd-generate` 支持全部生成、分级生成、部分生成、更新和模板入库 |
| 全流程检查 | `/prd-check` 或 `checks/scripts/check-all.py` 顺序运行四个模块检查 |

## 怎么用

### Step 0：安装

推荐直接安装到当前项目：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

安装器界面由 `skills@latest` 控制，可能显示英文。常用操作是：

| 操作 | 含义 |
|------|------|
| `↑` / `↓` | 上下移动 |
| `Space` | 勾选或取消 |
| `Enter` | 确认 |

安装时选择 `prd-helper`，再选择你要使用的编码 Agent，例如 Claude Code、Codex、Trae。这个仓库只提供一个完整 Skill，所以安装后只看到 `/prd-helper` 是正常的。

### Step 1：初始化项目

安装完成后，在 Agent 对话中运行：

```text
/prd-helper
```

它会自动初始化或修复当前项目：

- 创建默认文档目录 `docs/prd-helper/`
- 写入 `CLAUDE.md`、`AGENTS.md` 或 Trae `project_rules.md` 中的 PRD Helper 配置块
- 为 Claude Code 生成 `.claude/commands/prd-start.md` 等项目级斜杠命令
- 为 Codex 安装 `~/.codex/plugins/prd-helper/` 插件命令
- 准备 `01-collect/active/`、`01-collect/passive/`、`source-index.md`、`collect-state.md`

如果 Claude Code 刚生成命令后没有立即显示 `/prd-start`，重开一次 Claude Code 会话再输入 `/prd-start`。如果还是没有，检查：

```bash
ls .claude/commands/prd-*.md
```

### Step 2：采集材料

开启主动采集：

```text
/prd-start
```

主动采集只在显式开启后生效，不会默认采集所有会话。采集状态命令：

| 命令 | 用途 |
|------|------|
| `/prd-start` | 开启主动采集 |
| `/prd-pause` | 暂停主动采集，并清理 Claude Code Hook |
| `/prd-resume` | 恢复主动采集，并重新启用 Claude Code Hook |
| `/prd-stop` | 停止采集，生成采集摘要和检查；Codex 会扫描 JSONL 会话做兜底补录 |
| `/prd-status` | 查看当前采集状态 |

被动材料直接放入：

```text
docs/prd-helper/01-collect/passive/
```

采集模块只保存原貌、建立索引、标记元信息和可能噪音，不做事实提取，也不生成 PRD。

### Step 3：精炼为用户故事

采集完成后进入 Refine。输出结构以 US 目录为中心：

```text
docs/prd-helper/02-refine/
├── index.md
├── US-001-xxx/
│   ├── user-story.md
│   ├── facts.md
│   ├── decisions.md
│   ├── constraints.md
│   ├── goals.md
│   ├── conflicts.md
│   ├── questions.md
│   ├── assumptions.md
│   └── changelog.md
└── check.md
```

精炼阶段的重点是区分事实与推断、保留来源、暴露冲突和待确认问题。

### Step 4：建立关系网络

Relate 不再维护旧的 `page-map.md`、`feature-map.md`、`rule-map.md` 等扁平 map 文件，而是用 `relations.md` 表达网状关系：

```text
docs/prd-helper/03-relate/
├── relations.md
├── themes.md
├── decisions-trail.md
├── concept-hierarchy.md
├── context-map.md
└── check.md
```

标准关系类型包括：影响、约束、依赖、依据、包含、冲突、补充、触发。

### Step 5：生成 PRD

触发生成：

```text
/prd-generate
```

Generate 支持四种模式：

| 模式 | 说明 |
|------|------|
| 全部生成 | 一次生成 Agent 维度和人类维度全部产物 |
| 分级生成 | 先生成 Agent 维度，再生成人类维度，方便中途审查 |
| 部分生成 | 只生成指定部分，例如 pages、rules、data |
| 更新 | 检测输入变化后重新生成 |

输出结构：

```text
docs/prd-helper/04-generate/
├── agent/
│   ├── overview/
│   ├── pages/
│   ├── rules/
│   ├── data/
│   ├── acceptance/
│   ├── agent-context/
│   └── implementation/
├── human/
│   ├── system-prd.md
│   └── page-prd/
└── check.md
```

Agent 维度给代码 Agent 继续执行，Human 维度给产品、业务、评审和归档阅读。

### Step 6：全流程检查

在 Agent 中运行：

```text
/prd-check
```

也可以在仓库根目录手动运行：

```bash
python3 checks/scripts/check-all.py docs/prd-helper
```

单模块检查命令：

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

## 常用命令

| 命令 | 用途 |
|------|------|
| `/prd-helper` | 初始化或修复当前项目 |
| `/prd-start` | 开启主动采集 |
| `/prd-pause` | 暂停主动采集 |
| `/prd-resume` | 恢复主动采集 |
| `/prd-stop` | 停止采集并生成采集摘要 |
| `/prd-status` | 查看采集状态 |
| `/prd-generate` | 生成 PRD，支持模板入库和多种生成模式 |
| `/prd-check` | 运行四模块检查并汇总结果 |
| `/prd-remove` | 卸载 PRD Helper 并清理 Agent 配置 |

## 卸载

在 Agent 对话中运行：

```text
/prd-remove
```

卸载会清理 Agent 配置块、Claude Code 命令、Claude Hook、Codex 插件引用，并调用 `skills remove` 删除 Skill。默认保留 `docs/prd-helper/`，避免误删业务文档。

## 项目结构

```text
PRDContextEngine/
├── SKILL.md                       # Skill 根入口
├── modules/
│   ├── collect/                   # 采集模块
│   ├── refine/                    # 精炼模块：US + 实体
│   ├── relate/                    # 关联模块：relations + themes
│   └── generate/                  # 生成模块：agent + human
├── checks/                        # 横向质量门禁
│   └── scripts/check-all.py       # 全流程检查入口
├── scripts/
│   ├── setup-prd-helper.py        # 初始化
│   ├── remove-prd-helper.py       # 卸载
│   └── lib/                       # 共享库
├── support/
│   ├── adapters/                  # Claude Code / Codex / Trae 适配器
│   └── assets/                    # README 图片资源
├── docs/adr/                      # 架构决策记录
└── tests/                         # 自动化测试
```

## 开发检查

开发或调整 Skill 后建议运行：

```bash
python3 -m py_compile scripts/*.py scripts/lib/*.py modules/*/scripts/*.py checks/scripts/*.py
python3 -m pytest tests
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
```

## 设计约束

- 单仓库、单 Skill、四模块，不把 collect/refine/relate/generate 拆成四个 Skill。
- 原始材料先保存原貌，噪音只做轻量标记，清洗留给 Refine。
- 主动采集必须由 `/prd-start` 显式开启。
- Refine 必须区分事实、决策、约束、冲突、问题和 AI 推断。
- Relate 使用 `relations.md` 表达网状关系，不回退到旧的五个 map 文件。
- Generate 必须基于 `02-refine/` 和 `03-relate/`，不能凭空新增业务规则。
- 每个阶段都必须保留来源、状态、待确认项和检查结果。
