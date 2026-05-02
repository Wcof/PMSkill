# PRD Helper

![PRD Helper Skill Kit overview](support/assets/prd-helper-project-overview.svg)

一句话：PRD Helper 是一个可安装的 Agent Skill，把产品讨论、会议纪要、客户反馈和旧文档，按“采集、精炼、关联、生成”四个模块转成可追溯的 PRD 上下文。

安装器界面由 `skills@latest` 控制，当前可能显示英文；安装完成后，`prd-helper` 会跟随用户语言输出，中文用户默认中文，英文用户默认英文，无法判断时会先询问语言。

## 项目介绍

PRD Helper 不是一个普通脚本包，也不是四个分散的小工具。它是一个完整的 Skill：根目录的 `SKILL.md` 是唯一入口，`modules/` 显式承载四个业务模块，`checks/` 提供贯穿全流程的质量门禁，`scripts/` 提供安装、采集、检查和卸载自动化。

四个模块的职责是：

| 模块 | 目标 | 产物 |
|------|------|------|
| Collect 采集 | 保存原始材料，支持主动会话采集和被动文件投放 | `01-collect/`、`source-index.md`、`collect-state.md` |
| Refine 精炼 | 从原始材料中拆出事实、目标、决策、约束、问题和 AI 推断 | `02-refine/` |
| Relate 关联 | 建立事实到页面、功能、规则、数据、验收的关系链 | `03-relate/`、`context-map.md` |
| Generate 生成 | 输出前端、后端、测试、产品可使用的 PRD 和 Agent 上下文 | `04-generate/`、`05-check/` |

检查不是第五个业务模块；它是每一步都必须执行的质量门禁。

## 怎么用

### Step 0：安装 Skill

推荐使用免交互安装，避免安装器英文提示干扰：

```bash
npx skills@latest add Wcof/PRDContextEngine --all
```

如果你想手动选择 Agent，也可以运行交互式安装器：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

安装器会让你选择 Skill 和编码 Agent。这个仓库只提供一个完整 Skill：`prd-helper`，它内部已经包含四个模块，不需要分别安装 collect、refine、relate、generate。

交互方式：

| 操作 | 说明 |
|------|------|
| `↑` / `↓` | 上下移动 |
| `Space` | 勾选或取消 |
| `Enter` | 确认 |

建议默认全选：

- Skill：`prd-helper`
- Agent：你当前项目会用到的全部编码 Agent，例如 Codex、Claude Code、Trae
- 首次入口：`/prd-init`

安装完成后，在 Agent 对话中运行：

```text
/prd-init
```

首次运行 `/prd-init` 会自动初始化项目。初始化会完成：

- 创建 PRD Helper 文档目录，默认 `docs/prd-helper/`
- 写入 `CLAUDE.md`、`AGENTS.md` 或 Trae `project_rules.md` 中的 PRD Helper 配置块
- 在 Claude Code 项目中生成 `.claude/commands/prd-start.md` 等真实斜杠命令文件
- 设置主动采集策略：默认只在 `/prd-start` 后采集

完成后，项目会准备好 `docs/prd-helper/` 结构。

### 安装后快速自检

初始化完成后，建议立刻做一次最小自检：

```text
/prd-status
```

看到采集状态（capture_mode/session_id/turn_count）即可说明命令入口和项目初始化已生效。

### Step 1：开始采集

在 Agent 对话中运行：

```text
/prd-start
```

开启后，Agent 会把会话按 `User Query + Agent Answer` 写入主动采集目录。

已有材料直接放入被动采集目录：

```text
docs/prd-helper/01-collect/passive/
```

适合投放的材料包括会议纪要、评审记录、客户反馈、旧 PRD、原型说明、历史 Agent 会话摘要等。

### Step 2-4：完成四模块闭环

采集完成后，按顺序推进：

```text
Collect 采集 → Refine 精炼 → Relate 关联 → Generate 生成
```

每一步都要留下可追溯来源、状态、待确认项和检查结果。最终产物默认保存在：

```text
docs/prd-helper/
```

## 常用命令

| 命令 | 用途 |
|------|------|
| `/prd-init` | 初始化当前项目配置和 `docs/prd-helper/` 结构 |
| `/prd-start` | 开启主动采集 |
| `/prd-pause` | 暂停主动采集 |
| `/prd-resume` | 恢复主动采集 |
| `/prd-stop` | 停止采集，并生成采集摘要和检查 |
| `/prd-status` | 查看采集状态 |
| `/prd-remove` | 卸载 PRD Helper，并清理 Agent 配置引用 |

## 卸载

在 Agent 对话中运行：

```text
/prd-remove
```

卸载会先清理当前项目中的 Agent 配置块，例如 `AGENTS.md`、`CLAUDE.md`、Trae `project_rules.md`，再调用 `skills remove` 删除 Skill。只执行 `skills remove` 不会清理这些配置引用。

卸载默认保留已经生成的 `docs/prd-helper/` 项目文档，避免误删业务资产。

## 运行检查

在仓库根目录运行：

```bash
python3 modules/collect/scripts/check-collect.py --root examples/robot-inspection/docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py examples/robot-inspection/docs/prd-helper
python3 modules/relate/scripts/check-relate.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-structure.py examples/robot-inspection/docs/prd-helper
python3 modules/generate/scripts/check-generated.py examples/robot-inspection/docs/prd-helper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
```

开发时建议同时运行：

```bash
python3 -m py_compile scripts/*.py scripts/lib/*.py modules/*/scripts/*.py
python3 -m pytest tests
```

## 项目结构

```text
PRDContextEngine/
├── SKILL.md              # Skill 根入口，Agent 首先读取这里
├── modules/              # 四个业务模块
│   ├── collect/          # 采集：主动会话 + 被动材料
│   │   └── scripts/      # 采集脚本：控制、采集、扫描、检查
│   ├── refine/           # 精炼：事实、决策、约束、问题、推断
│   │   └── scripts/      # 精炼检查脚本
│   ├── relate/           # 关联：页面、功能、规则、数据、验收链路
│   │   └── scripts/      # 关联检查脚本
│   └── generate/         # 生成：PRD、Agent 上下文、验收材料
│       └── scripts/      # 生成检查脚本
├── checks/               # 横向质量门禁，不是第五业务模块
├── scripts/              # 全局脚本：安装、卸载、配置清理、结构检查
│   └── lib/              # 共享库：状态、索引、ID、路径、哈希等
├── examples/             # 可运行示例
├── support/              # Agent 适配器、安装说明、图片资源
├── CONTEXT.md            # 领域词汇表
└── docs/adr/             # 架构决策记录
```

## 设计约束

- 单仓库、单 Skill、四模块，不把四个模块拆成四个 Skill。
- 原始材料先保存原貌，噪音只做轻量标记，清洗留给精炼模块。
- 主动采集必须由 `/prd-start` 显式开启，不默认采集所有会话。
- 每个决策、约束、推断和生成文档都要能追溯到来源。
- 安装和卸载都优先通过 Agent 斜杠命令完成，降低新手使用门槛。
