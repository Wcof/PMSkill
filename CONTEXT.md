# PMSkill Context

产品经理在 Agent 里工作的 Skill 工具箱。从模糊想法/用户诉求出发，沉淀成清晰的 PMContext，
再转成可交付的 PRD（给 AI 或给人）和草图（多种可视化形态）。

## Language

**PM（产品经理）**:
在 Agent（Claude/Codex/Trae 等）里工作的产品经理，自己用 Agent 协作完成需求工作。
_Avoid_: 只写文档不协作的 PM、纯对接工程的 PM

**/pm-setup**:
user-invoked。首次使用 PMSkill 时配置项目。运行一次即可，后续 Skill 自动读取配置。
流程：
1. **Explore**：检查项目现有状态——`docs/pm-context/` 是否已存在？AGENTS.md/CLAUDE.md 是否有 PMSkill 配置？当前 Agent 类型。
2. **Ask**（一次一个）：产物目录（默认 `docs/pm-context/`）→ 语言偏好（中文/英文/双语）→ Agent 类型（Claude Code/Codex/Trae）。
3. **Write**：创建目录 + 在 AGENTS.md 或 CLAUDE.md 写入极简 Agent 规则段：
```markdown
## PMSkill
- 领域术语：见 CONTEXT.md
- 产物目录：docs/pm-context/
- PMContext（唯一 Entity）：docs/pm-context/pm-context.md
```
不注册 hook——/pm-collect 从对话上下文直接收集，不需要拦截 Agent 会话。
_Avoid_: 重复安装器已负责的命令注册、预判模板偏好、注册 hook

**/pm-need**:
user-invoked 主入口。PM 手敲 `/pm-need`，一口气走完 collect → refine，产出 PMContext。
内含 /pm-collect 和 /pm-refine 两个子步骤，也可单独调用。
_Avoid_: 把 /pm-need 拆成更多子命令、让 /pm-need 跳过追问直接落盘

**/pm-collect**:
model-invoked。把零散想法、用户反馈、会议纪要、历史会话捞进来。
优先从对话中收集（PM 在对话里说/粘贴），也支持导入已有文件/文件夹。
收集后 AI 整理到 `docs/pm-context/collect/` 目录，按材料类型聚合为一个 md 文件（避免文件过多增加大模型理解成本）：
```markdown
# <类型名>（如：会议纪要）
## <具体材料1标题>
### 来源索引
- 来源：对话 / 文件导入 / 历史会话
- 路径：<原始文件路径，如果是文件导入>
- 时间：<收集时间>
### 概要
<一段话总结>
### 关键信息
- <关键点1>
- <关键点2>
### 与其他材料的关联
- 与 <材料X> 互相印证/矛盾
## <具体材料2标题>
...
```
整理时建立材料之间的关联（如：同一主题的多条反馈、互相印证或矛盾的材料）。
可被 /pm-need 调用，也可独立使用（PM 只想先存材料不急着澄清）。
_Avoid_: 在 collect 阶段就提取事实或改写原文、原样堆文件不整理、不建立材料间关联、一个材料一个文件导致文件过多

**/pm-refine**:
model-invoked。对已收集材料追问澄清，区分事实/假设/冲突/待确认，沉淀成 PMContext。
核心纪律：一次一个追问，走完每个分支，Agent 提供推荐答案（继承 grilling）。
追问按 PM 追问维度进行，确保不遗漏关键产品决策：
1. **用户场景**：每个功能点追问"谁在什么场景下用？达到什么目的？"
2. **边界条件**：追问异常路径——"如果 X 失败呢？""如果用户同时做 Y 呢？"
3. **优先级**：追问"必须做 vs 最好有""MVP 边界在哪？"
4. **冲突检测**：不同来源/陈述矛盾时追问"以哪个为准？"
5. **术语澄清**：PM 用模糊词时追问"你说的 X 具体指什么？"
6. **现状平替与摩擦力**：追问"在没有这个功能之前，用户目前用什么土办法凑合？土办法里最痛苦的点（Friction）是什么？"——搞清 Workaround 才能找到 ROI 最高的解法。
7. **技术与资源约束**：追问"这个交互对延迟的要求？是否涉及高昂 Token 成本或硬件限制？"——现代产品（尤其 AI 驱动）不能脱离物理约束谈需求。
8. **价值验证度量**：追问"上线后看哪个指标证明做对了？指标没变是否意味着可以下线？"——强迫 PM 从功能交付导向转向业务价值导向。
追问时主动建立事实与规则、页面、验收之间的关联，确保 PMContext 内部无孤立项。
可被 /pm-need 调用，也可独立使用（PM 手里已有材料，跳过 collect 直接澄清）。
追问终止机制：Agent 每走完一个分支后汇报"剩余 N 个未澄清方向"，PM 决定继续还是喊停落盘。
_Avoid_: Agent 自行判断追问完成、PM 无进度信息地瞎飞、沉淀出孤立项不关联、跳过追问维度

**PMContext（产品经理上下文）**:
/pm-refine 追问澄清后沉淀的结构化、可追溯上下文。整个工作流的唯一 Entity（源）。
所有 PRD 和草图都从它衍生。落盘为单文件 `pm-context.md`，用 heading 分段，自包含——下游 Skill 读一个文件就知道全貌。
Heading 按业务领域组织（关系隐含在层级里）：
```markdown
# PMContext: <需求名>
## 概述
### 问题与目标
### 现状平替与摩擦力
### 价值验证度量
## <页面/功能名>（如：用户登录）
### 事实
### 规则
### 验收
## <页面/功能名>（如：支付流程）
### 事实
### 规则
### 验收
## 全局约束
## 风险项 [待确认] [假设] [冲突]
```
PMContext 是活文档——产品认知在迭代，PMContext 跟着迭代。PM 拿到新反馈后可再次调用 /pm-refine，
Agent 读现有 PMContext + 新材料，只追问新增部分，增量写入。PRD 和草图也支持重新生成覆盖旧版本。
版本历史由 git 承担，不需要内置版本化。
PMContext 内部用显式标记区分确定性内容与风险内容：
`[待确认]` 标记需进一步确认的项，`[假设]` 标记 Agent 推断，`[冲突]` 标记矛盾。
View（PRD/草图）忠实反映这些标记，未确认项不能写成确定性要求。
追溯简化为"有来源 / 无来源"一级：每项内容要么行内标注来源（`← 来源: 某轮追问`），要么无来源。
无来源的项自动标 `[假设]`。不再区分 Strong/Weak Trace 二级——追问中产出的内容天然有定位。
_Avoid_: 原始材料的堆放（那是采集产物不是上下文）、不可追溯的会议纪要、单独的检查报告、Strong/Weak Trace 二级追溯、拆成多文件

**/pm-prd**:
user-invoked。从 PMContext 同时输出给 AI 和给人的两种 PRD 形态。
生成时确保每条需求都追溯到 PMContext 中的具体项，无来源的需求标 `[待确认]`。
内含 /pm-aiprd 和 /pm-humanprd 两个子步骤，也可单独调用。
_Avoid_: 跳过 PMContext 直接从聊天生成 PRD、需求项无追溯

**/pm-aiprd**:
model-invoked。从 PMContext 输出给 AI 的 PRD，带 Agent Context，供 Agent 执行。
结构：
```
ai-prd.md
├── 概述（Overview）         ← 一段话说清楚要做什么、为什么
├── Agent Context            ← Agent 执行所需的关键上下文
│   ├── 技术栈与约束
│   ├── 目录结构约定
│   └── 关键模块位置
├── 用户故事（User Stories）  ← 从 PMContext 衍生，带场景和验收标准
├── 实施规则（Rules）         ← 从 PMContext 衍生，确定性要求
├── 数据模型（Data）          ← 关键实体和字段
├── 验收标准（Acceptance）    ← 每个用户故事怎么算做完
├── 风险项（Risks）           ← [待确认]/[假设]/[冲突] 标记的内容
└── 超出范围（Out of Scope）  ← 明确不做的事
```
_Avoid_: 不带追溯信息、把待确认项写成确定性要求

**/pm-humanprd**:
model-invoked。从 PMContext 输出给人的 PRD，供人类阅读评审。
与 ai-prd.md 同源同骨架，但写法针对人类读者调整：
```
human-prd.md
├── 概述（Overview）         ← 完整背景 + 决策理由
├── 用户故事（User Stories）  ← 自然语言，加业务价值说明
├── 实施规则（Rules）         ← 决策表 + "为什么这样决定"
├── 数据模型（Data）          ← 实体关系说明
├── 验收标准（Acceptance）    ← 场景描述
├── 风险项（Risks）           ← 标记 + 影响分析
└── 超出范围（Out of Scope）  ← 列表 + 排除理由
```
_Avoid_: 塞入 Agent Context 等机器可读内容

**PRD（需求文档）**:
PMContext 的下游 View 之一，结构化需求文档。分两种形态：
给 AI 的 PRD（/pm-aiprd 产物）和给人的 PRD（/pm-humanprd 产物）。
_Avoid_: 把 PRD 当 Entity、凭空从聊天直接生成 PRD

**/pm-sketch**:
user-invoked。从 PMContext 输出全部四种草图，默认全出。
画图时确保每个图元都对应 PMContext 中的实体/关系，无法对应的图元标 `[假设]`。
内含 /pm-wireframe、/pm-ia、/pm-state、/pm-flow 四个子步骤，也可单独调用。
_Avoid_: 脱离 PMContext 凭感觉画图、图元无追溯

**/pm-wireframe**:
model-invoked。从 PMContext 输出界面线框图。
产出格式：Mermaid flowchart 画页面间导航关系 + markdown 表格画每个页面内的组件布局（区域 | 组件 | 交互）。
两个维度互补——图擅长导航流，表格擅长布局细节。
_Avoid_: 不基于 PMContext 中的页面/功能定义、只用 Mermaid 画布局（表达力不足）

**/pm-ia**:
model-invoked。从 PMContext 输出信息架构图。
产出格式：Mermaid graph/flowchart，节点为实体/页面，边为导航/包含关系。
_Avoid_: 不基于 PMContext 中的实体/关系定义

**/pm-state**:
model-invoked。从 PMContext 输出状态机图。
产出格式：Mermaid stateDiagram-v2，状态节点 + 转移边 + 条件标注。
_Avoid_: 不基于 PMContext 中的状态/转移定义

**/pm-flow**:
model-invoked。从 PMContext 输出流程图。
产出格式：Mermaid flowchart，步骤节点 + 判断分支 + 异常路径。
_Avoid_: 不基于 PMContext 中的步骤/顺序定义

**草图（Sketch）**:
PMContext 的下游 View 之一，可视化形态。以 markdown 内嵌图（Mermaid 等）表达，Agent 可直接读写。
包括界面线框图、信息架构图、状态机、流程图等。
草图与 PRD 平级，都从 PMContext 衍生，不互相嵌套。草图的可读对象包括 Agent 自己。
_Avoid_: 把草图当 PRD 的插图、脱离 PMContext 凭感觉画图、输出 SVG/PNG 等二进制格式

**View（视图）**:
PRD 和草图的统称——都是 PMContext 的下游表达，不是独立的领域实体。
_Avoid_: 把任何文档类型升级成 Entity

**Entity（领域实体）**:
只有 PMContext 是 Entity：它是源头，需要被引用、需要 ID、参与追溯链路。
PRD 和草图都是 View。
_Avoid_: 因为某类文档有文件就把它升级成实体

## Skill 调用关系

- **/pm-setup**（user-invoked）首次配置项目，后续 Skill 自动读取。
- **/pm-need**（user-invoked）编排 **/pm-collect** 和 **/pm-refine**（model-invoked）。
- /pm-collect 和 /pm-refine 也可独立调用。
- 追问终止：Agent 汇报剩余未澄清分支，PM 决定停止并落盘。
- **/pm-prd**（user-invoked）编排 **/pm-aiprd** 和 **/pm-humanprd**（model-invoked）。
- /pm-aiprd 和 /pm-humanprd 也可独立调用。
- **/pm-sketch**（user-invoked）编排 **/pm-wireframe**、**/pm-ia**、**/pm-state**、**/pm-flow**（model-invoked），默认全出。
- 四个草图子 Skill 也可独立调用。
- **关联增强**：旧项目 Relate 阶段已去掉，关联纪律分散进所有环节——collect 建材料间关联，refine 建事实/规则/页面/验收关联，prd 确保需求追溯到 PMContext，sketch 确保图元对应实体/关系。

## Skill 目录结构

```
skills/
  setup/                    ← 初始化
    pm-setup/SKILL.md
  discovery/                ← 需求发现
    pm-need/SKILL.md
    pm-collect/SKILL.md
    pm-refine/SKILL.md
  delivery/                 ← 交付
    pm-prd/SKILL.md
    pm-aiprd/SKILL.md
    pm-humanprd/SKILL.md
  visualization/            ← 可视化
    pm-sketch/SKILL.md
    pm-wireframe/SKILL.md
    pm-ia/SKILL.md
    pm-state/SKILL.md
    pm-flow/SKILL.md
```

不需要 `/pm-remove`——不注册 hook 无需清理，Agent 规则几行手动删，产物目录可能有价值不自动删，Skill 卸载归安装器。

## SKILL.md Frontmatter

| Skill | type | description |
|---|---|---|
| pm-setup | user-invoked | 首次使用 PMSkill 时配置项目（目录/语言/Agent 规则） |
| pm-need | user-invoked | 从模糊想法或用户诉求出发，收集材料并追问澄清，沉淀成 PMContext |
| pm-collect | model-invoked | 收集零散想法、用户反馈、会议纪要、历史会话。Use when the user mentions feedback, meeting notes, or wants to save raw materials before refining. |
| pm-refine | model-invoked | 对已收集材料追问澄清，沉淀成 PMContext。Use when collected materials exist and need clarification, or when the user wants to sharpen requirements. |
| pm-prd | user-invoked | 从 PMContext 生成 PRD 文档（给 AI 和给人两种形态） |
| pm-aiprd | model-invoked | 从 PMContext 生成给 AI 执行的 PRD。Use when another skill needs Agent-executable PRD, or the user asks for AI-ready PRD. |
| pm-humanprd | model-invoked | 从 PMContext 生成给人阅读的 PRD。Use when the user asks for a human-readable PRD or review document. |
| pm-sketch | user-invoked | 从 PMContext 生成全部草图（线框/信息架构/状态机/流程图） |
| pm-wireframe | model-invoked | 从 PMContext 生成界面线框图。Use when the user asks for wireframe or page layout. |
| pm-ia | model-invoked | 从 PMContext 生成信息架构图。Use when the user asks for information architecture or entity relationships. |
| pm-state | model-invoked | 从 PMContext 生成状态机图。Use when the user asks for state machine or state transitions. |
| pm-flow | model-invoked | 从 PMContext 生成流程图。Use when the user asks for flowchart or process flow. |

user-invoked 设置 `disable-model-invocation: true`，description 人看一句话；model-invoked 不设置，description 带 "Use when..." trigger phrasing。

## SKILL.md Body 约定

user-invoked 编排入口极简（参考 skills 项目 grill-me 只有 3 行）：
- `/pm-need`：Run `/pm-collect` to gather materials, then run `/pm-refine` to question and clarify, producing PMContext.
- `/pm-prd`：Run `/pm-aiprd` and `/pm-humanprd` to produce both PRD forms from PMContext.
- `/pm-sketch`：Run `/pm-wireframe`, `/pm-ia`, `/pm-state`, and `/pm-flow` to produce all sketches from PMContext.
- `/pm-setup`：流程已在上方定义（Explore → Ask → Write）。

model-invoked Skill 的 body 包含完整纪律和流程（它们是可被独立调用的复用单元）。

## Relationships

- **PM** 产出 **PMContext**（唯一 Entity）。
- **PMContext** 衍生出两类 **View**：**PRD** 和 **草图**。
- **PRD** 有两种形态：给 AI 的、给人的。
- **草图** 有多种形态：界面线框、信息架构图、状态机、流程图等。
- 所有 View 必须可追溯到 **PMContext**，不可凭空生成。

## 产物目录布局

```
docs/pm-context/
  pm-context.md          ← Entity（唯一）
  collect/               ← /pm-collect 整理后的材料
  prd/                   ← PRD View
    ai-prd.md            ← /pm-aiprd 产物
    human-prd.md         ← /pm-humanprd 产物
  sketch/                ← 草图 View（每个图一个独立 md）
    wireframe.md
    ia.md
    state.md
    flow.md
```

## Flagged Ambiguities

- "采集/精炼/关联/生成"四阶段是旧项目概念，仅作参考，已被 PMContext 主链路取代。
- "草图"不等于"PRD 的配图"——它是独立 View，和 PRD 平级。
- Soft Gate / 独立检查机制已去掉，改为 PMContext 内显式标记（[待确认]/[假设]/[冲突]），View 忠实反映。
