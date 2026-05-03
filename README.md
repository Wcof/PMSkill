# PRD Helper

![PRD Helper Skill Kit overview](support/assets/prd-helper-project-overview.svg)

一句话：PRD Helper 是一个可安装的单体 Agent Skill，把产品讨论、会议纪要、客户反馈、旧文档和 Agent 会话，按“采集、精炼、关联、生成”四个模块转成可追溯的 PRD 上下文。

安装器界面由 `skills@latest` 控制，当前可能显示英文；安装完成后，`prd-helper` 会跟随用户语言输出，中文用户默认中文，英文用户默认英文，无法判断时会先询问语言。

## 项目介绍

PRD Helper 不是一个普通脚本包，也不是四个分散的小 Skill。它是一个完整 Skill：根目录的 `SKILL.md` 是唯一入口，`modules/` 显式承载四个业务模块，`checks/` 提供贯穿全流程的质量门禁，`scripts/` 提供安装、采集、检查和卸载自动化。

四个模块的职责是：

| 模块 | 目标 | 产物 |
|------|------|------|
| Collect 采集 | 保存原始材料，支持主动会话采集和被动文件投放 | `01-collect/`、`source-index.md`、`collect-state.md` |
| Refine 精炼 | 从原始材料中拆出事实、目标、决策、约束、问题和 AI 推断 | `02-refine/` |
| Relate 关联 | 建立事实到页面、功能、规则、数据、验收的关系链 | `03-relate/`、`context-map.md` |
| Generate 生成 | 输出前端、后端、测试、产品可使用的 PRD 和 Agent 上下文 | `04-generate/`、`05-check/` |

检查不是第五个业务模块；它是每一步都必须执行的质量门禁。

当前能力边界：

| 场景 | 当前实现 | 说明 |
|------|----------|------|
| 安装 | `npx skills@latest add Wcof/PRDContextEngine` | 安装器只会发现一个 Skill：`prd-helper`，这是预期行为 |
| 初始化 | `/prd-helper` | 初始化项目目录、Agent 配置块、Claude 命令文件和 Codex 插件 |
| Claude Code 主动采集 | `.claude/commands/` + `.claude/settings.json` hooks | `/prd-start`/`/prd-resume` 启用 Hook，`/prd-pause`/`/prd-stop` 清理 Hook |
| Codex 主动采集 | `~/.codex/plugins/prd-helper/` + JSONL 会话兜底 | Codex 没有进程级 Hook，`/prd-stop` 会扫描当前项目的 Codex 会话补录 |
| 被动采集 | `docs/prd-helper/01-collect/passive/` | 会议纪要、评审记录、旧 PRD、客户反馈等文件直接放这里 |

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

安装器会让你选择 Skill 和编码 Agent。这个仓库只提供一个完整 Skill：`prd-helper`，所以刚安装完只看到 `/prd-helper` 是正常的。它内部包含采集、精炼、关联、生成四个模块，不需要分别安装 collect、refine、relate、generate。

交互方式：

| 操作 | 说明 |
|------|------|
| `↑` / `↓` | 上下移动 |
| `Space` | 勾选或取消 |
| `Enter` | 确认 |

建议默认全选：

- Skill：`prd-helper`
- Agent：你当前项目会用到的全部编码 Agent，例如 Codex、Claude Code、Trae
- 首次入口：`/prd-helper`

安装完成后，在 Agent 对话中运行：

```text
/prd-helper
```

运行 `/prd-helper` 会自动初始化或修复当前项目。初始化会完成：

- 创建 PRD Helper 文档目录，默认 `docs/prd-helper/`
- 写入 `CLAUDE.md`、`AGENTS.md` 或 Trae `project_rules.md` 中的 PRD Helper 配置块
- 在 Claude Code 项目中生成 `.claude/commands/prd-start.md` 等真实斜杠命令文件
- 在 Codex 项目中安装 `~/.codex/plugins/prd-helper/` 插件，注册原生斜杠命令
- 设置主动采集策略：默认只在 `/prd-start` 后采集，Hook 在 `/prd-start`/`/prd-resume` 时启用，在 `/prd-pause`/`/prd-stop` 时清理

完成后，项目会准备好 `docs/prd-helper/` 结构。Claude Code 的斜杠命令列表通常在会话启动时加载，所以刚生成 `.claude/commands/prd-start.md` 后，可能需要开启新会话或刷新命令列表才会显示 `/prd-start` 等命令。

如果重开会话后仍然只看到 `/prd-helper`，先检查当前项目是否生成了命令文件：

```bash
ls .claude/commands/prd-*.md
```

如果没有看到 `prd-start.md`，说明项目处于半初始化状态。再次发送 `/prd-helper`，它会幂等补齐 `.claude/commands/` 下的命令文件；补齐后重开 Claude Code 会话再输入 `/prd-start`。如果文件存在但命令列表仍不刷新，这是 Claude Code 本地命令缓存问题，不是 Skill 未安装。

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

开启后，Claude Code 会写入 `.claude/settings.json` hooks，并把后续会话按 `User Query + Agent Answer` 自动写入主动采集目录。`/prd-start` 本身只开启状态，不会采集开启命令这一轮。发送 `/prd-pause` 或 `/prd-stop` 后，Hook 会被清理，不再常驻生效。

### Codex 采集机制

Codex 没有 Claude Code 那种进程级 Hook，采用混合采集方案：

1. **Codex 插件命令**：安装时写入 `~/.codex/plugins/prd-helper/`，提供 `/prd-start`、`/prd-stop` 等命令入口
2. **AGENTS.md 指令注入**：采集模式开启时，每轮回答后 Agent 调用 `capture-source.py` 记录对话
3. **JSONL 会话扫描兜底**：`/prd-stop` 时自动扫描 `~/.codex/sessions/` 下的 JSONL 会话文件，补录未采集的轮次

Codex 会话数据存储在 `~/.codex/sessions/YYYY/MM/DD/rollout-{时间}-{uuid}.jsonl`，格式为 JSONL，每行一个 JSON 对象。扫描脚本通过 `session_meta.cwd` 过滤当前项目的会话，提取 `role=user` 和 `role=assistant` 的消息对。

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
| `/prd-helper` | 初始化或修复当前项目配置、`docs/prd-helper/` 结构和 Claude Code 后续命令 |
| `/prd-start` | 开启主动采集，并启用 Claude Code 采集 Hook |
| `/prd-pause` | 暂停主动采集，并清理 Claude Code 采集 Hook |
| `/prd-resume` | 恢复主动采集，并重新启用 Claude Code 采集 Hook |
| `/prd-stop` | 停止采集，清理 Claude Code 采集 Hook，并生成采集摘要和检查 |
| `/prd-status` | 查看采集状态 |
| `/prd-remove` | 卸载 PRD Helper，并清理 Agent 配置引用 |

## 卸载

在 Agent 对话中运行：

```text
/prd-remove
```

卸载会先清理当前项目中的 Agent 配置块，例如 `AGENTS.md`、`CLAUDE.md`、Trae `project_rules.md`，同时移除 Claude Code 命令、Claude Hook 和 Codex 插件引用，再调用 `skills remove` 删除 Skill。只执行 `skills remove` 不会清理这些配置引用。

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
│   └── lib/              # 共享库：状态、索引、ID、常量、哈希等
├── examples/             # 可运行示例
├── support/              # Agent 适配器、安装说明、图片资源
│   └── adapters/         # Claude Code、Codex、Trae 适配器
│       └── codex/plugin/ # Codex 插件结构（commands、agents）
├── CONTEXT.md            # 领域词汇表
└── docs/adr/             # 架构决策记录
```

## 开发说明

仓库根目录是唯一源码。安装器在项目中生成的 `.agents/`、`.claude/` 和 `skills-lock.json` 都是本地安装产物，不参与提交，也不作为脚本真实来源。开发和修复时只改仓库根目录下的 `SKILL.md`、`modules/`、`scripts/`、`support/`、`checks/`、`tests/` 等源码文件。

脚本共享边界：

- `scripts/lib/constants.py` 统一保存默认路径、命令名和生成目录结构等静态配置。
- `scripts/lib/markdown_util.py` 统一解析 Markdown 表格，`state.py` 和 `source_index.py` 只处理各自领域语义。
- `scripts/lib/id_registry.py` 是实体类型、ID 前缀、必填字段和实体生命周期的唯一注册表。
- Claude Code 采集 Hook 由 `scripts/lib/claude_hooks.py` 管理，`/prd-start`、`/prd-resume` 启用，`/prd-pause`、`/prd-stop`、`/prd-remove` 清理。
- Codex 会话发现由 `scripts/lib/codex_discovery.py` 管理，`/prd-stop` 时扫描 JSONL 补录未采集轮次。

## 设计约束

- 单仓库、单 Skill、四模块，不把四个模块拆成四个 Skill。
- 原始材料先保存原貌，噪音只做轻量标记，清洗留给精炼模块。
- 主动采集必须由 `/prd-start` 显式开启，不默认采集所有会话。
- 每个决策、约束、推断和生成文档都要能追溯到来源。
- 安装和卸载都优先通过 Agent 斜杠命令完成，降低新手使用门槛。
