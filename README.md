# PRD Helper

[中文](README.md) | [English](README.en.md)

![PRD Helper 项目介绍图](support/assets/prd-helper-project-overview.svg)

## 一句话价值

PRD Helper 是一个 **PRD Context Compiler（PRD 上下文编译流程）**：把分散在会议、聊天、评审和旧文档里的产品上下文，沉淀成可追溯、可检查、可复用的结构化 PRD 资产和 **Agent Context** 工程指导文件。

它坚持一条主链路：**采集（Collect）→ 精炼（Refine）→ 关联（Relate）→ 生成（Generate）**。检查（Check）是横向 **Soft Gate（软门禁）**，不是第五阶段；Soft Gate 不默认阻断用户命令，但会暴露来源缺失、断链和待确认风险。

## 它解决什么问题

很多团队不是没有需求资料，而是资料散、来源乱、版本多，最后 PRD 变成“谁记得就听谁的”。PRD Helper 的目标是让 Agent 和团队先保存原始材料，再精炼信息、建立关系，最后生成 PRD 和指导人或 Agent 实施的 Agent Context，避免直接让 AI 从碎片聊天里凭感觉写文档。

如果用户跳过前置阶段或检查未通过，`/prd-generate` 仍可执行，但结果属于 **Limited Generate（受限生成）**：缺失来源、断链、待确认问题和禁止实施项必须显式标记，不能伪装成完整确定性 PRD。

生成阶段的文档文件是 **View**，不是 **Entity**。只有跨阶段流转、需要被引用、需要 ID、需要参与关系链路的对象，才是领域实体。来源追溯也分级：具备 `source_id + path + quote/paraphrase + locator` 的内容是 **Strong Trace**；缺少 locator 的内容是 **Weak Trace**，不能进入确定性要求。

## 当前指令清单

当前权威指令集合来自 `scripts/lib/command_registry.py`、`skills/prd-*/SKILL.md`、`commands/*.md` 和插件声明。`npx skills@latest add Wcof/PRDContextEngine` 会发现并安装以下 11 个命令 Skill：

| 指令 | 阶段/类型 | 作用 | 主要产物 |
|---|---|---|---|
| `/prd-helper` | 初始化入口 | 初始化或修复当前项目配置，创建 `docs/prd-helper/` 和 Agent 规则 | 配置、目录、Agent 规则 |
| `/prd-start` | 采集 | 开启主动采集，后续产品讨论会写入采集区 | `01-collect/active/`、`collect-state.md` |
| `/prd-stop` | 采集 | 停止主动采集，清理采集 Hook，并生成采集摘要和检查结果 | `collect-summary.md`、`01-collect/check.md` |
| `/prd-status` | 采集工具 | 查看当前采集状态、session、写入目录和计数 | 状态摘要 |
| `/prd-scan` | 采集工具 | 批量扫描历史 Agent 会话并导入采集池 | `01-collect/active/historical/`、`source-index.md` |
| `/prd-import` | 采集工具 | 导入第三方文件夹作为被动材料，不提前清洗原文 | `01-collect/passive/`、`source-index.md` |
| `/prd-refine` | 精炼 | 从采集材料中提炼事实、背景、目标、决策、约束、冲突、问题和推断 | `02-refine/` |
| `/prd-relate` | 关联 | 建立事实、页面、功能、规则、数据、验收之间的上下游关系 | `03-relate/` |
| `/prd-generate` | 生成 | 基于精炼与关联产物生成 PRD 文档和 Agent 上下文 | `04-generate/` |
| `/prd-discuss` | 辅助研讨 | 在采集和精炼之间追问矛盾、模糊术语和未决问题，每次只追问一个问题 | 研讨摘要、待确认项 |
| `/prd-remove` | 卸载 | 清理 PRD Helper 项目配置、命令和 Hook，默认保留已生成文档 | 清理结果 |

平台说明：`skills/` 目录包含上述 11 个安装器可发现的 Skill。`COMMAND_NAMES` 仍只记录除 `/prd-helper` 外的 10 个后续命令，用于项目级兜底命令和卸载清理。

## 工程约束

PRD Helper 遵循“Python 执行化，静态提示词约束化”：

- 指令事实来自 `scripts/lib/command_registry.py`，`COMMAND_NAMES`、安装脚本和一致性测试都从这里派生。
- 业务规则保留在 `skills/prd-helper/SKILL.md`、`modules/*/guide.md` 和 `commands/*.md`，Python 不承担提示词职责。
- 产物结构和检查清单优先放在 `modules/*/templates/`，脚本只填入状态、计数、检查结果和来源信息。

## 快速开始

### 1. 安装命令 Skills

```bash
npx skills@latest add Wcof/PRDContextEngine
```

安装器会从 `skills/` 目录发现 `prd-helper`、`prd-start`、`prd-stop`、`prd-status`、`prd-scan`、`prd-import`、`prd-refine`、`prd-relate`、`prd-generate`、`prd-discuss`、`prd-remove`。交互模式里选择这些 Skill，并选择你要安装到的 Agent，例如 Claude Code、Codex 或 Trae。

### 2. 初始化当前项目

在 Agent 会话中输入：

```text
/prd-helper
```

初始化会创建默认目录 `docs/prd-helper/`，并补齐 Agent 规则、项目级兜底命令和 Hook 配置。后续命令已在安装时注册；`/prd-helper` 不是它们出现的前置条件。

### 3. 按四阶段推进

```text
/prd-start    # 开启主动采集
/prd-stop     # 停止主动采集并生成采集摘要
/prd-scan     # 扫描历史 Agent 会话
/prd-import   # 导入第三方文件夹作为被动材料
/prd-refine   # 精炼采集材料
/prd-relate   # 建立上下游关系链路
/prd-generate # 生成 PRD 文档和 Agent 上下文
```

需要查看状态时用 `/prd-status`，需要研讨模糊点时用 `/prd-discuss`，需要卸载时用 `/prd-remove`。

主动采集内容会进入：

```text
docs/prd-helper/01-collect/active/
```

手动材料放入：

```text
docs/prd-helper/01-collect/passive/
```

## 四阶段工作流

| 阶段 | 目录 | 做什么 | 不做什么 |
|---|---|---|---|
| Collect 采集 | `modules/collect/` | 保存原始材料、建立索引、记录 hash、维护采集状态 | 不提前改写事实、不生成规则 |
| Refine 精炼 | `modules/refine/` | 区分事实、背景、目标、决策、约束、冲突、问题、推断 | 不把推断写成事实、不跳到 PRD |
| Relate 关联 | `modules/relate/` | 建立 `fact -> page/feature -> rule -> data/acceptance` 链路 | 不让事实、规则、数据、验收断链 |
| Generate 生成 | `modules/generate/` | 生成 PRD、验收、数据说明和 Agent 上下文 | 不新增未来源化、未关联的业务规则 |

### Generate 如何保证一次性生成完整

Generate 现在采用 manifest-driven 流程，不再只依赖 Agent 按提示词手动补文件：

1. **Generate Manifest** 从 `02-refine/` 和 `03-relate/` 推导应输出的完整 View 清单，包括 overview、pages、rules、data、acceptance、4 份 Agent Context 和 `check.md`。
2. **Generate Runner** 执行 `manifest -> scaffold/generate -> check`，创建缺失 View，保留已有用户内容，并输出 created/existing/skipped/limited/failed 摘要。
3. **Quality Report** 驱动 `04-generate/check.md`，检查覆盖率、模板完整性、Traceability、Relation Chain、Agent Context Safety 和 Limited Generate 风险。

因此，“是否生成完所有 PRD”以 Generate Manifest 为准，而不是只检查当前目录里已经存在的文件。

## 检查命令

这些是脚本级质量门禁，不是斜杠指令：

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

## 常见问题

只看到 `/prd-helper`，没有 `/prd-start`：这通常表示安装时只选择了 `prd-helper`，或当前 Agent 没刷新 Skill 列表。重新运行 `npx skills@latest add Wcof/PRDContextEngine` 并安装全部 `prd-*` Skill；已打开的会话可能仍需重开。即使菜单未刷新，直接输入 `/prd-start` 也会由已安装 Skill 或项目级兜底命令执行。Codex 的 hooks 会在 `/prd-start` 写入 `.codex/hooks.json`，并在 `/prd-stop` 清理。

采集没有写入：先运行 `/prd-status`，确认状态是 `on`；再检查 `docs/prd-helper/01-collect/collect-state.md`。

不知道先用 `/prd-scan` 还是 `/prd-import`：历史 Agent 会话用 `/prd-scan`；第三方文件夹、会议纪要、旧 PRD、客户反馈用 `/prd-import` 或直接放入 `01-collect/passive/`。

不想继续使用：运行 `/prd-remove`，它会清理项目配置、命令和 Hook，但默认保留已经生成的 `docs/prd-helper/` 文档。

## 开源协作

- 贡献指南：`CONTRIBUTING.md`
- 行为准则：`CODE_OF_CONDUCT.md`
- 安全策略：`SECURITY.md`
- 支持方式：`SUPPORT.md`
- 版本记录：`CHANGELOG.md`
- GitHub 介绍图 Prompt 指南：`docs/github-project-kit.md`
