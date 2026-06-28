# PMSkill

产品经理在 Agent 里工作的 Skill 工具箱。

从模糊想法/用户诉求出发，**一键全链路**沉淀成 PMContext → 衍生出 PRD（给 AI + 给人）→ 生成可视化草图 + HTML 可交互原型。

> 经过 darwin-skill 9 轮结构化优化 + 参考 [pm-skills (PM Compass)](https://github.com/phuryn/pm-skills) 最佳实践，13 个 SKILL.md 全量覆盖角色设定、产出示例、延伸参考与实战提示。符合 [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)：YAML frontmatter 渐进披露、第三人称触发描述、Level 3 references 按需加载。

## 一句话价值

PMSkill 帮助在 Agent 里工作的产品经理，把分散的模糊产品上下文，通过**零确认全自动链路**沉淀成可追溯的 PMContext，再从 PMContext 衍生出可交付的 PRD 和草图。

## 快速开始

### 1. 安装

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. 初始化（仅一次）

```text
/pm-setup
```

### 3. 一键全链路（推荐）

一句话触发 collect → refine → PRD → 原型，零确认：

```text
/pm-need <需求描述> --auto
```

示例：`/pm-need 会员体系重构 --auto`

### 4. 分步执行

```text
/pm-need              # 全自动收集材料 + 推断澄清 → 产出 PMContext，停在审计门
/pm-prd               # 从 PMContext 生成 PRD（给 AI + 给人）
/pm-prd --auto        # 零确认模式：直接出 PRD，不暂停
/pm-sketch            # 从 PMContext 生成全部草图
/pm-sketch --prototype # 生成 Mermaid 草图 + HTML 可交互原型
```

## 核心主张

**PMContext 是唯一 Entity（源），PRD 和草图都是它的下游 View。**

- PMContext 落盘为单文件 `pm-context.md`，自包含，下游 Skill 读一个文件就知道全貌
- PRD 有两种形态：给 AI 的（带 Agent Context，供 Agent 直接执行）和给人的（供人类评审）
- 草图以 markdown 内嵌 Mermaid 图表达，Agent 可直接读写
- HTML 原型（`--prototype`）单页无外部依赖，断网可预览，9 项质量检查
- 风险信息用显式标记（`[待确认]`/`[假设]`/`[冲突]`）写在正文里，不需要独立检查报告

## 主链路

```
模糊想法/用户诉求
        │
  /pm-need ─── {--auto: 零确认} ───→ PMContext (唯一 Entity)
        │                                   │
  ┌─────┴─────┐                    ┌────────┴────────┐
  │           │                    │                 │
/pm-prd    /pm-premortem     /pm-sketch          /pm-sketch --prototype
  │           │                    │                 │
  ▼           ▼                    ▼                 ▼
prd/*.md   premortem.md      sketch/*.md       prototype.html
```

## Skill 清单

### Setup — 初始化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-setup` | user-invoked | 首次配置项目（产物目录/语言/知识库/Agent 规则） |

### Discovery — 需求发现

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-need` | user-invoked | 🏆 主入口：collect → refine → audit 全自动完成。`--auto` 零确认直达 PRD+原型 |
| `/pm-collect` | model-invoked | 主动深扫描（代码/git/URL/知识库），4 源去重，**不筛选只整理** |
| `/pm-refine` | model-invoked | 8 维度自主推断（P0 用户场景/边界/冲突 → P1 优先级/术语/摩擦力 → P2 技术约束/度量），标记置信度 |

### Delivery — 交付

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-prd` | user-invoked | 编排输出双形态 PRD。`--auto` 零确认，`--skip-ai`/`--skip-human` 可选 |
| `/pm-aiprd` | model-invoked | 给 AI 的 PRD：可执行规则 + 数据模型 + Agent Context + 验收标准 + 风险项 |
| `/pm-humanprd` | model-invoked | 给人的 PRD：决策理由 + 自然语言叙事 + 追溯清单，评审友好 |
| `/pm-premortem` | model-invoked | Pre-Mortem 风险分析：Tiger（真实风险）/Paper Tiger（过虑）/Elephant（未讨论）三分 + 行动计划 |

### Visualization — 可视化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-sketch` | user-invoked | 🏆 主入口：输出全部四类草图 + HTML 原型（`--prototype`）。`--auto` 零确认 |
| `/pm-wireframe` | model-invoked | 界面线框图：Mermaid 页面导航 + Markdown 表格组件布局 |
| `/pm-ia` | model-invoked | 信息架构图：Mermaid graph，实体/页面 + 导航/包含/引用三类边 |
| `/pm-state` | model-invoked | 状态机图：Mermaid stateDiagram-v2，状态 + 转移条件 + 异常路径 |
| `/pm-flow` | model-invoked | 流程图：Mermaid flowchart，步骤 + 判断 + 异常，循环配退出条件 |

## Skill 调用规则

- **user-invoked**：只能由人类触发（`disable-model-invocation: true`），可调用 model-invoked 子 skill
- **model-invoked**：可由 Agent 自主触发或由 user-invoked 编排调用
- user-invoked **不可**调用另一个 user-invoked skill

## 零确认模式（--auto）

所有 user-invoked 技能均支持 `--auto` 参数：

```text
/pm-need <需求> --auto        # 全链路：collect → refine → PRD → 原型，零确认
/pm-prd --auto                # 直接按已有 PMContext 生成 PRD，不暂停
/pm-sketch --auto             # 直接生成全部草图 + HTML 原型
```

`--auto` 模式下：
- 不等待 PM 确认，直接落盘所有产物
- 子 skill 失败不阻塞全链路，失败项单独标注
- 输出一站式报告含置信度分布 + 信息缺口，供 PM 事后审计

## /pm-refine 推断维度（8 维全覆盖）

```
P0（必须先推断）：
1. 用户场景    2. 边界条件    3. 冲突检测

P1（决定质量上限）：
4. 优先级（ICE/RICE/Kano）    5. 术语澄清    6. 现状平替与摩擦力

P2（增量增强）：
7. 技术与资源约束    8. 价值验证度量
```

## 失败模式处理

所有 Skill 统一采用 **三段式 fallback 表**（触发条件 → 一线修复 → 仍失败兜底）：

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 不存在 | 🔴 STOP：提示先运行 `/pm-need` | 不阻塞，提示后退出 |
| 子 skill 生成失败 | 不阻塞主流程，失败项单独标注 | 其他成功部分仍落盘 |
| 材料/信息不足 | 🟡 WARNING 标记到信息缺口 + 降置信度 | 不臆造，继续处理 |

## 产物目录

```
docs/pm-context/
  pm-context.md          ← 唯一 Entity（源）
  collect/               ← /pm-collect 整理后的原始材料
  prd/
    ai-prd.md            ← 给 AI 的 PRD（Agent 可执行）
    human-prd.md         ← 给人的 PRD（评审友好）
  sketch/
    wireframe.md         ← 界面线框图（Mermaid + 表格）
    ia.md                ← 信息架构图（Mermaid graph）
    state.md             ← 状态机图（Mermaid stateDiagram-v2）
    flow.md              ← 流程图（Mermaid flowchart）
    prototype.html       ← HTML 可交互原型（--prototype 模式）
```

## 项目结构

```
PMSkill/
├── INSTALL.md                    ← 本地直接安装入口（非 Skill，无 frontmatter）
├── CLAUDE.md                     ← Agent 指令 + 项目级 Skill 规则
├── CONTEXT.md                    ← 领域术语表
├── README.md                     ← 本文件
├── .claude-plugin/plugin.json    ← Claude Code 插件清单
├── .codex-plugin/plugin.json     ← Codex 插件清单
├── skills/
│   ├── setup/
│   │   ├── README.md             ← bucket 导航
│   │   └── pm-setup/
│   │       ├── SKILL.md          ← Level 1+2 渐进披露
│   │       └── references/       ← Level 3 按需加载
│   ├── discovery/
│   │   ├── README.md
│   │   ├── pm-need/SKILL.md + references/
│   │   ├── pm-collect/SKILL.md + references/
│   │   └── pm-refine/SKILL.md
│   ├── delivery/
│   │   ├── README.md
│   │   ├── pm-prd/SKILL.md
│   │   ├── pm-aiprd/SKILL.md
│   │   ├── pm-humanprd/SKILL.md
│   │   └── pm-premortem/SKILL.md
│   └── visualization/
│       ├── README.md
│       ├── pm-sketch/SKILL.md + references/
│       ├── pm-wireframe/SKILL.md
│       ├── pm-ia/SKILL.md
│       ├── pm-state/SKILL.md
│       └── pm-flow/SKILL.md
└── docs/
    ├── pm-context/            ← PMSkill 产物目录（运行后生成）
    └── adr/                   ← 架构决定记录

evals/                          ← 评估集（≥3 场景/skill + rubric）
├── README.md                   ← 评估方法说明
├── pm-*.json                   ← 13 个 skill 的评估场景
└── fixtures/                   ← 评估夹具（PMContext 样本/矛盾材料等）
```

## 渐进披露

本项目遵循 [Anthropic Agent Skills 三层渐进披露规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)：

| 层级 | 加载时机 | Token 开销 | 内容 |
|---|---|---|---|
| Level 1: Metadata | 始终（启动时） | ~100 tokens/skill | YAML frontmatter `name` + `description` |
| Level 2: Instructions | Skill 被触发时 | < 5k tokens | SKILL.md body（流程/失败模式/反例黑名单） |
| Level 3: Resources | 按需引用 | 无上限 | `references/` 下的产出示例、延伸参考、实战提示 |

每个 skill 的 references 文件按内容语义命名（如 `scan-recipes.md`/`inference-dimensions.md`/`flow-example.md`），便于 Claude 按需精准定位而非千篇一律的 `examples-and-tips.md`。

## 评估集

遵循 [Anthropic「先建评估再写文档」原则](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration)，每个 skill 在 `evals/` 下有 ≥3 个评估场景与可判定 rubric，夹具样本在 `evals/fixtures/`。详见 [evals/README.md](evals/README.md)。

## 延伸参考

本项目受以下资源启发：

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [PM Skills Marketplace (68 PM skills)](https://github.com/phuryn/pm-skills)
- [Continuous Discovery Habits - Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [A Proven AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Mermaid 官方文档](https://mermaid.js.org/)
- [Pre-Mortem: Meta/Instagram 实践](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## 设计决定

关键架构决定（记录在仓库 `docs/adr/`，本地开发可见，安装包不含）：

- **ADR 0004**: PMContext 是唯一 Entity，PRD 和草图都是 View
- **ADR 0005**: 显式标记替代 Soft Gate，风险写在正文里
- **ADR 0006**: Relate 阶段分散进所有 Skill，关联是每个 Skill 的内置纪律
- **ADR 0007**: 单级追溯（有来源/无来源）替代 Strong/Weak Trace 二级

## 常见问题

**PMContext 可以更新吗？** 可以。PMContext 是活文档，拿到新反馈后再次调用 `/pm-refine`，Agent 只推断新增部分，增量写入。

**可以跳过 collect 直接 refine 吗？** 可以。`/pm-collect` 和 `/pm-refine` 都可以独立调用。

**可以只出一种 PRD / 一种草图吗？** 可以。各子 skill 均可独立调用。

**--auto 模式和正常模式有什么区别？** 正常模式产出 PMContext 后停在审计门等 PM 确认；`--auto` 模式不等待，一气呵成全部落盘，事后出具一站式报告供审计。

**需要 /pm-remove 吗？** 不需要。不注册 hook 无需清理，Agent 规则手动删，产物目录可能有价值不自动删。

**支持哪些 Agent？** 所有 skills-compatible runtime：Claude Code、Codex、Cursor、Trae、OpenClaw、Hermes 等。安装命令自动适配，无需手动指定路径。
