# PRD Helper

![PRD Helper 项目导览图](support/assets/prd-helper-project-overview.svg)

[中文](#中文) | [English](#english)

---

## 中文

### 一句话价值

PRD Helper 把分散的产品讨论与文档，转成可追溯、可检查、可复用的结构化 PRD 资产，减少需求丢失和跨角色沟通成本。

### 这个项目解决什么问题

- 原始材料很散：会议纪要、聊天记录、评审结论、旧文档分布在多处。
- 需求不可追溯：最后 PRD 很难回溯“这条规则从哪来”。
- AI 直接生成容易幻觉：跳过采集和精炼会导致误解和漏项。
- 团队协作不一致：产品、研发、测试看到的上下文版本不统一。

### 核心能力（功能 + 用处）

| 功能 | 用处 | 解决的问题 |
|---|---|---|
| `/prd-helper` 初始化 | 幂等创建项目配置、命令、采集目录 | 安装后命令不可用、项目未就绪 |
| `/prd-start` `/prd-pause` `/prd-resume` `/prd-stop` | 显式控制主动采集状态，并维护采集状态文件 | 采集边界不清、会话遗漏 |
| Claude Hook 自动记录（start/resume 时启用） | 自动落盘 User Query + Agent Answer | 人工复制粘贴成本高、遗漏多 |
| `/prd-scan` 批量扫描 | 扫描多工具历史 session 进入采集池 | 历史上下文不连续 |
| 被动材料目录 `01-collect/passive/` | 手工投放会议纪要/评审记录/旧 PRD | 非会话材料无法纳管 |
| 四模块流程（Collect/Refine/Relate/Generate） | 先收集、再提炼、再建关系、最后生成 | 直接生成 PRD 的质量波动 |
| 各阶段 check 脚本 | 每个阶段都有可执行检查 | 文档完整性和可追溯性无法验证 |
| `/prd-grill` 压力测试模式 | 对采集内容做矛盾/模糊点挑战，更新 CONTEXT/ADR | 术语不清、决策未固化 |
| `/prd-remove` 卸载 | 清理项目配置和命令入口 | 安装残留与污染 |

### 项目结构（你会常用到的）

```text
PRDContextEngine/
├── SKILL.md
├── modules/
│   ├── collect/
│   ├── refine/
│   ├── relate/
│   └── generate/
├── commands/
│   ├── prd-helper.md
│   ├── prd-start.md ... prd-remove.md
├── scripts/
│   ├── setup-prd-helper.py
│   ├── remove-prd-helper.py
│   └── lib/
└── support/assets/
```

### 怎么用（推荐路径）

#### 1) 安装

```bash
npx skills@latest add Wcof/PRDContextEngine
```

> 安装器界面通常是英文：`↑/↓` 移动，`Space` 勾选，`Enter` 确认。

#### 2) 初始化（首次必做）

在 Agent 会话中执行：

```text
/prd-helper
```

初始化后应可见（或可执行）命令：

```text
/prd-start
/prd-pause
/prd-resume
/prd-stop
/prd-status
/prd-scan
/prd-grill
/prd-remove
```

#### 3) 开始采集

```text
/prd-start
```

- 主动会话会进入 `docs/prd-helper/01-collect/active/`
- 被动材料放入 `docs/prd-helper/01-collect/passive/`
- 历史会话补采可用：

```text
/prd-scan
```

#### 4) 按四模块推进

1. Collect: `modules/collect/guide.md`
2. Refine: `modules/refine/guide.md`
3. Relate: `modules/relate/guide.md`
4. Generate: `modules/generate/guide.md`

#### 5) 运行检查（示例）

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

### 常见问题（快速排错）

- 只看到 `/prd-helper`，没有 `/prd-start`：先执行一次 `/prd-helper` 完成项目初始化；必要时重开会话刷新命令列表。
- 安装后命令没出现：确认当前目录是项目目录，且安装时选中了目标 Agent。
- 采集没写入：确认已 `/prd-start`，`/prd-status` 为 `on`，并检查 `docs/prd-helper/01-collect/collect-state.md`。

---

## English

### One-line Value

PRD Helper turns scattered product discussions and docs into traceable, checkable, reusable PRD assets, reducing requirement loss and cross-team misalignment.

### What Problem This Solves

- Raw context is fragmented across meetings, chats, reviews, and legacy docs.
- Final PRDs are often not traceable to source evidence.
- Direct AI generation can hallucinate when collection/refinement is skipped.
- Product, engineering, and QA frequently work from different context versions.

### Core Capabilities (Feature + Why It Matters)

| Feature | Why it matters | Problem solved |
|---|---|---|
| `/prd-helper` init | Idempotent setup of config, commands, and folders | Skill installed but project not ready |
| `/prd-start` `/prd-pause` `/prd-resume` `/prd-stop` | Explicit control of active capture lifecycle | Unclear capture boundaries |
| Claude hook auto-capture | Writes User Query + Agent Answer to docs | Manual copy/paste loss |
| `/prd-scan` batch import | Imports historical sessions from multiple tools | Broken historical continuity |
| Passive intake folder | Drop meeting notes / feedback / old PRDs | Non-chat sources unmanaged |
| 4-stage workflow | Collect -> Refine -> Relate -> Generate | Quality drift from direct generation |
| Stage checks | Scripted validation per stage | No quality gate for outputs |
| `/prd-grill` mode | Challenge ambiguities and contradictions, update CONTEXT/ADR | Vague terminology, weak decisions |
| `/prd-remove` uninstall | Cleans project-level setup and command entries | Residual config pollution |

### Project Layout

```text
PRDContextEngine/
├── SKILL.md
├── modules/{collect,refine,relate,generate}
├── commands/
├── scripts/
└── support/assets/
```

### How to Use

#### 1) Install

```bash
npx skills@latest add Wcof/PRDContextEngine
```

#### 2) Initialize (required once per project)

Run in your agent session:

```text
/prd-helper
```

Then you should have:

```text
/prd-start /prd-pause /prd-resume /prd-stop /prd-status /prd-scan /prd-grill /prd-remove
```

#### 3) Start collection

```text
/prd-start
```

- Active chat capture goes to `docs/prd-helper/01-collect/active/`
- Passive files go to `docs/prd-helper/01-collect/passive/`
- Import existing sessions with:

```text
/prd-scan
```

#### 4) Execute the 4 modules

1. Collect: `modules/collect/guide.md`
2. Refine: `modules/refine/guide.md`
3. Relate: `modules/relate/guide.md`
4. Generate: `modules/generate/guide.md`

#### 5) Run checks (example)

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

### Troubleshooting

- Only `/prd-helper` appears: run `/prd-helper` once to initialize project commands, then reopen session if needed.
- Commands not visible after install: confirm you installed to the current agent and current project scope.
- No capture output: verify `/prd-status` is `on` and inspect `docs/prd-helper/01-collect/collect-state.md`.
