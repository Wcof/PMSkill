# PRD Helper 规范规则

以下是所有 agent 平台必须遵循的核心规则。各适配器从此文件引用，不再各自重复。

## 核心规则

1. **产品上下文处理必须走 prd-helper skill 流程。**
2. **不允许直接从原始材料生成最终 PRD，必须保留中间产物。**
3. **必须区分事实、推断、冲突、待确认。**
4. **不允许把 AI 推断当成确定事实。**
5. **不允许跳过来源、冲突、待确认问题。**
6. **必须运行检查。**
7. **必须输出 Context Delta。**

## 语言规则

安装器界面可能由 `skills@latest` 控制并显示英文；安装完成后，各 Agent 必须由 PRD Helper 规则接管语言：

- 用户主要使用中文时，默认中文输出，关键术语保留英文括注，例如“采集（Collect）”。
- 用户主要使用英文时，默认英文输出，关键模块首次出现时保留中文括注。
- 用户中英混合时，关键字段使用中英双语，正文跟随用户主要语言。
- 无法判断用户语言偏好时，第一次响应先询问：`请选择语言 / Choose language: 中文 or English`。
- `/prd-helper`、`/prd-start`、`/prd-status`、`/prd-remove` 的提示必须遵循同一语言策略。

## 工作流程

安装后触发 `/prd-helper` 时，Agent 必须自动执行初始化脚本。初始化脚本是幂等的：它会创建 `docs/prd-helper/`、写入 Agent 配置文件，并在 Claude Code / Codex 项目中补齐命令与采集配置。不要因为 `docs/prd-helper/prd-helper-config.md` 已存在就跳过 setup。Claude Code 与 Codex 的采集 hooks 都由 `/prd-start` 启用，由 `/prd-stop` 清理。

处理产品上下文时，必须按以下顺序执行：

1. **Collect（采集）**：保存原始上下文到 `docs/prd-helper/01-collect/`
   - 读取 `modules/collect/guide.md` 获取行为约束和验收条件
2. **Refine（精炼）**：提取事实、背景、目标、决策、约束、冲突、问题到 `docs/prd-helper/02-refine/`
   - 读取 `modules/refine/guide.md` 获取行为约束和验收条件
3. **Relate（关联）**：建立关系到 `docs/prd-helper/03-relate/`
   - 读取 `modules/relate/guide.md` 获取行为约束和验收条件
4. **Generate（生成）**：输出文档到 `docs/prd-helper/04-generate/`
   - 读取 `modules/generate/guide.md` 获取行为约束和验收条件
5. **Final Check（最终检查，不是第五个业务环节）**：输出到 `docs/prd-helper/05-check/`

## 检查要求

每一步完成后都必须运行检查：

- 采集后：`01-collect/check.md`
- 精炼后：`02-refine/check.md`
- 关联后：`03-relate/check.md`
- 生成后：`04-generate/check.md`
- 最终：`05-check/` 下的所有检查文件

## 采集命令

| 命令 | 含义 |
|------|------|
| `/prd-helper` | 初始化 PRD Helper：创建 docs 目录、启用 Agent、采集策略，并生成命令文件 |
| `/prd-start` | 开启 PRD Capture Session，并启用 Claude Code / Codex hooks 自动采集后续轮次 |
| `/prd-stop` | 停止采集，清理 Claude Code / Codex hooks，生成摘要和检查 |
| `/prd-status` | 查看采集状态 |
| `/prd-scan` | 扫描历史 Agent 会话并批量导入采集池 |
| `/prd-import` | 导入第三方文件夹数据作为被动材料 |
| `/prd-refine` | 精炼采集材料，提取事实、决策、约束、冲突、问题和推断 |
| `/prd-relate` | 建立事实、页面、功能、规则、数据、验收之间的关系 |
| `/prd-generate` | 生成结构化 PRD 文档和 Agent 上下文 |
| `/prd-discuss` | 进入需求研讨模式，追问矛盾、模糊术语和未决问题 |
| `/prd-remove` | 卸载 PRD Helper：先清理 Agent 配置引用，再卸载 Skill |

收到 `/prd-remove` 后，Agent 必须执行卸载脚本，不要求用户手动运行 shell 命令：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

如果是 Claude Code 项目，脚本路径通常是：

```bash
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

收到 `/prd-helper` 时，Agent 必须直接执行安装目录中的 setup 脚本，用它完成初始化或修复半初始化状态。只有用户明确要求自定义 docs 目录或 Agent 范围时，才先询问配置。默认配置如下：

- docs 目录：`docs/prd-helper/`
- Agent：当前正在使用的 Agent
- 采集策略：只在 `/prd-start` 后主动采集

默认脚本路径：

```bash
python3 .agents/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
```

## Context Delta

每次完成任务后，必须在 `docs/prd-helper/05-check/context-delta.md` 输出本轮上下文增量。

## 参考文件

- `SKILL.md` — 流程编排
- `modules/collect/guide.md` — 采集模块行为约束
- `modules/refine/guide.md` — 精炼模块行为约束
- `modules/relate/guide.md` — 关联模块行为约束
- `modules/generate/guide.md` — 生成模块行为约束
- `checks/guide.md` — 检查系统说明
- `scripts/lib/id_registry.py` — 实体 ID 注册表

## 模板

使用 `modules/*/templates/` 和 `checks/templates/` 下的模板文件。
