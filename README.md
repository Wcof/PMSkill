# PRD Helper

![一张图教会你 PRD Helper 项目](support/assets/prd-helper-project-overview.svg)

## 怎么用

### Step 0：安装

运行 skills.sh 安装器（installer）：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

选择你要安装的 Skill 和编码 Agent（coding agents）。这个仓库默认只提供一个完整 Skill：`prd-helper`，它内部包含采集、精炼、关联、生成四个业务模块，不需要分模块安装。

交互选择时：

- 使用 `↑` / `↓` 移动
- 使用 `Space` 勾选或取消
- 使用 `Enter` 确认
- 不需要输入数字

安装完成后，在你的 Agent 中运行：

```text
/prd-setup
```

它会询问并确认：

- 你要把 PRD Helper 文档保存在哪里，默认 `docs/prd-helper/`
- 你当前项目启用哪些 Agent，例如 Codex、Claude Code、Trae
- 采集策略是否只通过显式命令开启，默认只在 `/prd-start` 后主动采集

完成后就可以使用 `/prd-start` 开始采集。

### 卸载

安装完成后，在 Claude Code、Codex 或 Trae 对话中发送：

```text
/prd-remove
```

如果平台支持参数式斜杠命令，也可以发送：

```text
/remove prd-helper
```

Agent 会按顺序完成两件事：

- 清理 `AGENTS.md`、`CLAUDE.md`、Trae `project_rules.md` 中的 PRD Helper 配置块
- 执行 `skills remove` 卸载 `prd-helper` Skill

如果 Agent 无法执行斜杠命令，可以手动执行同等命令：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

Claude Code 项目通常使用：

```bash
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

底层卸载命令是：

```bash
npx skills@latest remove prd-helper --agent '*' -y
```

如果当初是全局安装，使用：

```bash
npx skills@latest remove prd-helper --agent '*' --global -y
```

如果你想手动选择要卸载的 Skill，可以运行：

```bash
npx skills@latest remove
```

交互卸载同样使用 `↑` / `↓` 移动，`Space` 勾选，`Enter` 确认，不需要输入数字。

`/prd-remove` 会先调用清理脚本，再调用 `skills remove`。只执行 `skills remove` 不会清理 Agent 配置文件里的引用。

卸载 Skill 不会自动删除已经生成的项目文档；如需清理产物，可以手动删除目标项目里的 `docs/prd-helper/`。

### Step 1：开始采集（Collect）

在你的项目中，向 Agent 发送：

```text
/prd-start
```

Agent 会创建采集目录，开始主动记录你的产品讨论。

投放已有材料（会议纪要、旧 PRD、客户反馈等），直接放到：

```text
docs/prd-helper/01-collect/passive/
```

采集完成后，Agent 会按流程执行：

```text
Step 1 采集（Collect）→ Step 2 精炼（Refine）→ Step 3 关联（Relate）→ Step 4 生成（Generate）
```

每一步都有自动检查，确保质量。

### 采集命令

| 命令 | 含义 |
|------|------|
| `/prd-start` | 开启采集 |
| `/prd-pause` | 暂停采集 |
| `/prd-resume` | 恢复采集 |
| `/prd-stop` | 停止采集，生成摘要和检查 |
| `/prd-status` | 查看当前采集状态 |
| `/prd-setup` | 初始化项目配置和 `docs/prd-helper/` 结构 |
| `/prd-remove` | 卸载 PRD Helper 并清理 Agent 配置 |

### 运行检查

```bash
python3 scripts/check-collect.py --root examples/robot-inspection/docs/prd-helper/01-collect
python3 scripts/check-refine.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-relate.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-structure.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-relations.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-generated.py examples/robot-inspection/docs/prd-helper
```

---

## 项目介绍

PRD Helper 是一个面向 Agent 的 PRD 上下文工程能力包。

它把零散的产品讨论、会议纪要、旧文档和 Agent 会话，沉淀成可追溯、可精炼、可关联、可生成、可检查的 PRD 上下文资产。

### 结构

```text
PRDContextEngine/
├── SKILL.md              # Skill 入口
├── modules/              # 四个业务模块
│   ├── collect/          # 采集：主动采集 + 被动采集
│   ├── refine/           # 精炼：提取事实、决策、约束
│   ├── relate/           # 关联：建立关系链路
│   └── generate/         # 生成：输出 PRD 和 Agent 上下文
├── checks/               # 质量门禁（不是第五业务模块）
├── scripts/              # 自动化脚本
└── examples/             # 示例项目
```

### 各部分职责

- `SKILL.md`：Skill 唯一入口，定义流程和执行约束。
- `modules/collect/`：采集模块，支持主动采集（`/prd-start`）和被动采集（投放文件）。
- `modules/refine/`：精炼模块，提取事实、目标、约束、冲突、问题与推断。
- `modules/relate/`：关联模块，建立需求到页面/功能/规则/数据/验收的链路。
- `modules/generate/`：生成模块，输出页面、规则、数据、验收、Agent 上下文文档。
- `checks/`：横向质量门禁，负责阶段检查与最终检查模板。
- `scripts/`：自动检查脚本和采集控制脚本。
- `examples/`：可直接参考的示例项目。
