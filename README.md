# PMSkill

产品经理在 Agent 里工作的 Skill 工具箱。

从模糊想法/用户诉求出发，沉淀成清晰的 PMContext，再转成可交付的 PRD（给 AI 或给人）和草图（多种可视化形态）。

## 一句话价值

PMSkill 帮助在 Agent 里工作的产品经理，把分散在脑中、对话、会议、反馈里的模糊产品上下文，通过追问澄清沉淀成可追溯的 PMContext，再从 PMContext 衍生出可交付的 PRD 和草图。

## 快速开始

### 1. 安装

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. 初始化

```text
/pm-setup
```

### 3. 按主链路推进

```text
/pm-need    # 收集材料 + 追问澄清 → 产出 PMContext
/pm-prd     # 从 PMContext 生成 PRD（给 AI + 给人）
/pm-sketch  # 从 PMContext 生成草图（线框/架构/状态机/流程图）
```

## 核心主张

**PMContext 是唯一 Entity（源），PRD 和草图都是它的下游 View。**

- PMContext 落盘为单文件 `pm-context.md`，自包含，下游 Skill 读一个文件就知道全貌
- PRD 有两种形态：给 AI 的（带 Agent Context，供 Agent 执行）和给人的（供人类阅读评审）
- 草图以 markdown 内嵌 Mermaid 图表达，Agent 可直接读写
- 风险信息用显式标记（`[待确认]`/`[假设]`/`[冲突]`）写在正文里，不需要独立检查报告

## 主链路

```
模糊想法/用户诉求
        ↓
  /pm-need (collect → refine)  →  PMContext (唯一 Entity)
        ↓                           ↓
  /pm-prd (ai + human)              /pm-sketch (wireframe + ia + state + flow)
        ↓                           ↓
  prd/ai-prd.md + prd/human-prd.md      sketch/*.md (Mermaid 内嵌图)
```

## Skill 清单

### Setup — 初始化

| Skill | 调用模型 | 作用 |
|---|---|---|
| `/pm-setup` | user-invoked | 首次配置项目（目录/语言/Agent 规则） |

### Discovery — 需求发现

| Skill | 调用模型 | 作用 |
|---|---|---|
| `/pm-need` | user-invoked | 主入口：collect → refine，产出 PMContext |
| `/pm-collect` | model-invoked | 收集材料（对话优先 + 文件导入），整理到 collect/ |
| `/pm-refine` | model-invoked | 追问澄清（8 个维度），沉淀成 PMContext |

### Delivery — 交付

| Skill | 调用模型 | 作用 |
|---|---|---|
| `/pm-prd` | user-invoked | 输出两种 PRD 形态 |
| `/pm-aiprd` | model-invoked | 输出给 AI 的 PRD（带 Agent Context） |
| `/pm-humanprd` | model-invoked | 输出给人的 PRD（评审友好） |

### Visualization — 可视化

| Skill | 调用模型 | 作用 |
|---|---|---|
| `/pm-sketch` | user-invoked | 输出全部四种草图 |
| `/pm-wireframe` | model-invoked | 界面线框图（Mermaid + 表格） |
| `/pm-ia` | model-invoked | 信息架构图（Mermaid graph） |
| `/pm-state` | model-invoked | 状态机图（Mermaid stateDiagram） |
| `/pm-flow` | model-invoked | 流程图（Mermaid flowchart） |

## /pm-refine 追问维度

1. **用户场景**：谁在什么场景下用？达到什么目的？
2. **边界条件**：异常路径——如果 X 失败呢？
3. **优先级**：必须做 vs 最好有，MVP 边界在哪？
4. **冲突检测**：不同来源矛盾时以哪个为准？
5. **术语澄清**：你说的 X 具体指什么？
6. **现状平替与摩擦力**：用户目前用什么土办法凑合？最痛苦的点是什么？
7. **技术与资源约束**：延迟要求？Token 成本？硬件限制？
8. **价值验证度量**：上线后看哪个指标证明做对了？

## 产物目录

```
docs/pm-context/
  pm-context.md          ← Entity（唯一）
  collect/               ← /pm-collect 整理后的材料
  prd/
    ai-prd.md            ← 给 AI 的 PRD
    human-prd.md         ← 给人的 PRD
  sketch/
    wireframe.md         ← 界面线框图
    ia.md                ← 信息架构图
    state.md             ← 状态机图
    flow.md              ← 流程图
```

## 设计决定

关键架构决定（记录在仓库 `docs/adr/`，本地开发可见，安装包不含）：

- **ADR 0004**: PMContext 是唯一 Entity，PRD 和草图都是 View
- **ADR 0005**: 显式标记替代 Soft Gate，风险写在正文里
- **ADR 0006**: Relate 阶段分散进所有 Skill，关联是每个 Skill 的内置纪律
- **ADR 0007**: 单级追溯（有来源/无来源）替代 Strong/Weak Trace 二级

## 常见问题

**PMContext 可以更新吗？** 可以。PMContext 是活文档，拿到新反馈后再次调用 `/pm-refine`，Agent 只追问新增部分，增量写入。

**可以跳过 collect 直接 refine 吗？** 可以。`/pm-collect` 和 `/pm-refine` 都可以独立调用。如果 PM 手里已有材料，直接 `/pm-refine`。

**可以只出一种 PRD 吗？** 可以。`/pm-aiprd` 和 `/pm-humanprd` 都可以独立调用。

**可以只出一种草图吗？** 可以。`/pm-wireframe`、`/pm-ia`、`/pm-state`、`/pm-flow` 都可以独立调用。

**需要 /pm-remove 吗？** 不需要。不注册 hook 无需清理，Agent 规则几行手动删，产物目录可能有价值不自动删，Skill 卸载归安装器。
