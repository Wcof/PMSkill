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
2. **Ask**（一次一个）：产物目录（默认 `docs/pm-context/`）→ 语言偏好（中文/英文/双语）→ 知识库路径（跳过 / 一个或多个本地目录路径）→ Agent 类型（Claude Code/Codex/Trae）。
3. **Write**：创建目录 + 在 AGENTS.md 或 CLAUDE.md 写入极简 Agent 规则段：
```markdown
## PMSkill
- 领域术语：见 CONTEXT.md
- 产物目录：docs/pm-context/
- PMContext（唯一 Entity）：docs/pm-context/pm-context.md
- 知识库：<用户指定路径，或"无">
```
不注册 hook——/pm-collect 从对话上下文 + 项目扫描 + 知识库搜索收集，不需要拦截 Agent 会话。
_Avoid_: 重复安装器已负责的命令注册、预判模板偏好、注册 hook

**/pm-need**:
user-invoked 主入口。PM 调用 `/pm-need <需求描述>`，`$ARGUMENTS` 可包含一句话需求和 URL 引用，全自动走完 collect → refine，产出 PMContext 后停在审计门等 PM 确认。
内含 /pm-collect 和 /pm-refine 两个子步骤，也可单独调用。
审计门输出：PMContext 置信度分布（事实/[假设]/[待确认]/[冲突]占比）+ 信息缺口清单 + 下一步选项。
_Avoid_: 把 /pm-need 拆成更多子命令、在 collect 和 refine 之间插入人工确认

**/pm-collect**:
model-invoked。主动收集材料，无需 PM 手动喂入。从四个来源自动扫描：
1. **URL 抓取**：从 `/pm-need` 的 `$ARGUMENTS` 中提取所有 URL，逐个抓取网页/文档内容。抓取失败标 `[待确认]`，不阻塞。来源标注为 `URL: <原始链接>`。
2. **对话上下文**：PM 在当前对话中说/粘贴的内容。
3. **项目扫描**：主动扫描当前项目的 README、docs/、CHANGELOG、近期 issue/PR 等，提取与产品需求相关的信息。
4. **知识库搜索**：若 /pm-setup 配置了知识库路径，搜索知识库中与当前需求相关的文档（竞品分析、用户调研、行业报告、历史 PRD 等），来源标注为 `知识库: <文件路径>`。
收集后 AI 整理到 `docs/pm-context/collect/` 目录，按材料类型聚合为一个 md 文件（避免文件过多增加大模型理解成本）：
```markdown
# <类型名>（如：会议纪要）
## <具体材料1标题>
### 来源索引
- 来源：URL / 对话 / 项目扫描 / 知识库
- 路径：<原始 URL 或文件路径>
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
可被 /pm-need 调用，也可独立使用。
完成后输出："收集了 N 条材料（来源：URL U 条 / 对话 M 条 / 项目扫描 K 条 / 知识库 L 条）"，无需 PM 确认。
_Avoid_: 在 collect 阶段就提取事实或改写原文、原样堆文件不整理、不建立材料间关联、一个材料一个文件导致文件过多

**/pm-refine**:
model-invoked。对已收集材料精炼澄清，区分事实/假设/冲突/待确认，沉淀成 PMContext。
**两种执行模式**，共享 8 维精炼骨架，差异在"推断不了时怎么办"：
- **追问模式**（默认）：Agent 对每个维度先尝试从材料推断；推断不了的项不直接标 `[待确认]`，而是逐一向 PM 提问澄清。PM 答复后回填为事实/[假设]/[冲突]。一次问一个问题，每个问题附 Agent 的推荐答案（对齐 grilling 纪律）。
- **自主推断模式**（`--auto` 触发）：Agent 自主推断，推断不了的标 `[待确认]` 记入信息缺口，PM 零介入。AI 在内部完成"自我追问 loop"——对每个维度自问自答，模拟追问但不外显。
核心规则：两种模式都先尝试从已有材料推断——有明确依据写为事实，不足但可推断写为推断并标 `[假设]` 附置信度(1-10)，完全缺失在追问模式下转为向 PM 提问、在自主模式下标 `[待确认]` 记入信息缺口，矛盾标 `[冲突]` 并选更可信来源附理由。
推断按 8 个维度进行，不可跳过：
1. **用户场景**：谁在什么场景下用？达到什么目的？
2. **边界条件**：追问异常路径——"如果 X 失败呢？""如果用户同时做 Y 呢？"
3. **优先级**：追问"必须做 vs 最好有""MVP 边界在哪？"推断时参考 ICE/RICE/Opportunity Score/Kano 框架辅助决策。
4. **冲突检测**：不同来源/陈述矛盾时追问"以哪个为准？"
5. **术语澄清**：模糊术语给出 Agent 理解的定义，标 `[假设]`
6. **现状平替与摩擦力**：追问"在没有这个功能之前，用户目前用什么土办法凑合？土办法里最痛苦的点（Friction）是什么？"——搞清 Workaround 才能找到 ROI 最高的解法。
7. **技术与资源约束**：追问"这个交互对延迟的要求？是否涉及高昂 Token 成本或硬件限制？"——现代产品（尤其 AI 驱动）不能脱离物理约束谈需求。
8. **价值验证度量**：追问"上线后看哪个指标证明做对了？指标没变是否意味着可以下线？"——强迫 PM 从功能交付导向转向业务价值导向。推断时参考度量设计准则：反映用户价值交付、可行动、可归因、优先比率型、配阈值、有采集时机、不超过 5 个。
推断时主动建立事实与规则、页面、验收之间的关联，确保 PMContext 内部无孤立项。
可被 /pm-need 调用，也可独立使用。独立调用默认追问模式，`--auto` 切自主。
_Avoid_: Agent 跳过推断维度、沉淀出孤立项不关联、追问模式一次问多个问题、追问模式不给推荐答案

**精炼（Refine）**:
pm-refine 的领域动作。把收集到的原始材料结构化为 PMContext 的过程，覆盖 8 维精炼骨架。
**精炼是单一动作，执行模式是正交维度**——追问模式和自主推断模式共享同一精炼骨架，只是"推断不了时"的处理路径不同。
_Avoid_: 把追问和精炼当成两个独立动作、把追问模式当成独立 skill

**追问模式（Discuss Mode）**:
pm-refine 的默认执行模式。Agent 对每个精炼维度先尝试从材料推断；推断不了的项转为向 PM 逐个提问，每个问题附 Agent 的推荐答案。PM 答复后回填为事实/[假设]/[冲突]。
纪律（对齐 grilling）：一次一个问题、能查代码/材料就查而不问、每个问题给推荐答案、走完 8 维设计树的每个分支。
**推荐答案格式（三段式）**：`推荐: <一句话答案> | 依据: <材料来源> | 备选: <1 个其它可能>`。备选不超过 1 个，逼迫 PM 在两个具体选项中选，降低开放式回答负担。
**PM 回答处理**：
- PM 说"对"/"选 A" → 采信推荐，标事实，来源记 `← 对话: PM 确认 + <原始材料>`
- PM 说"选 B" → 采信备选，标事实，来源记 `← 对话: PM 确认`
- PM 说"都不是，是 X" → 采信 X，标事实，来源记 `← 对话: PM 确认`，**不追问 X 的依据**（PM 是领域权威，逼依据破坏追问体验）
- 若 X 与现有材料矛盾 → 走 `[冲突]` 检测路径，标 `[冲突]` 附新旧两版来源，不反问 PM
由 pm-need 正常模式触发，或 pm-refine 独立调用时默认。
**退出机制**（C+A 组合）：
- **停（Stop）**：PM 说"停"/"先这样"/"我想再想想"即停。已问维度落盘 PMContext，未问维度强标 `[待确认]` 记入信息缺口。停=放弃追问、留缺口。
- **降级（Degraded）**：PM 说"剩下的你自主"/"你定吧"即降级为自主推断。未问维度走自主推断路径，可能标 `[假设]`（置信度更高）而非 `[待确认]`。降级=委托 Agent 推断、补缺口。
- Agent 检测"连续 3 个不知道/不确定"也触发降级，避免无意义追问。
**增量落盘纪律**：追问模式**不套用原子叠加**——每 2-4 个问题（或每完成一个精炼维度，取先到者）增量落盘 PMContext 已回填项。理由：追问是多轮对话，可能被中断/超时/上下文丢失，增量落盘避免信息丢失。落盘时只写已确认项，未问维度不写。
_Avoid_: 一次问多个问题、不给推荐答案就问、能查材料却问 PM、追问模式套用原子叠加导致中断丢信息、把"停"和"降级"混为一谈

**自主推断模式（Autonomous Mode）**:
pm-refine 的 `--auto` 执行模式。Agent 自主推断，推断不了的标 `[待确认]` 记入信息缺口，PM 零介入。
内部完成"自我追问 loop"——对每个维度自问自答，模拟追问的思考结构但不外显为对话。这是隐式推理，**不落盘对话日志**——结论走现有 `.loop/refine-step2/3/4.md` 路径，不新增 `.loop/refine-discuss-*.md`。审计三元组已提供可追溯性。
由 pm-need --auto 触发，或 pm-refine --auto 独立调用。
_Avoid_: 把自我追问 loop 外显为对话、把内部 loop 对话过程落盘到 .loop/（结论落盘，对话不落）、把对话日志当构建快照

**追问骨架（Grill Skeleton）**:
8 维精炼在追问模式下的提问序列结构。每维一个根问题 + 若干分支追问。根问题对应 8 维本身，分支追问对应"推断不了时的细化"。两种模式共享同一骨架——自主模式内部也按这个骨架自问自答。
_Avoid_: 追问模式自创问题序列偏离 8 维、自主模式跳过骨架的某维

**审计门优化（Audit Gate Optimization）**:
追问模式下审计门的呈现优化。追问模式中 PM 已逐维确认细节，审计门不再重复 8 维内容，转而聚焦全局元信息：置信度分布 + 信息缺口清单 + 项目扫描发现 + 下一步选项（进 PRD / 补材料 / 改 PMContext）。
**信息量不减，视角改变**——从"逐维细节确认"转为"全局全貌决策"。这不是精简（删内容），是优化（改呈现视角）。
与自主模式对称：自主模式审计门展示完整置信度（PM 未参与需看全貌），追问模式审计门优化呈现（PM 已参与只需看全局元信息 + 下一步）。
_Avoid_: 追问模式审计门重复 PM 刚答过的 8 维内容、把"优化"理解为删减信息量

**PMContext（产品经理上下文）**:
/pm-refine 自主推断澄清后沉淀的结构化、可追溯上下文。整个工作流的唯一 Entity（源）。
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
## 决策日志
| 决策点 | 选项A | 选项B | 最终选择 | 理由 | 来源 | 依据源数 | 工具名摘要 |
|--------|------|------|---------|------|------|---------|-----------|
## 假设清单与验证计划
| 假设 | 置信度(1-10) | 风险类型 | 验证方式 | 成功指标/阈值 | 验证时机 |
|------|------------|---------|---------|--------------|---------|
## 风险项 [待确认] [假设] [冲突]
## 信息缺口
- <维度>：<缺什么，建议 PM 补充什么>
```
PMContext 是活文档——产品认知在迭代，PMContext 跟着迭代。PM 拿到新反馈后可再次调用 /pm-refine，
Agent 读现有 PMContext + 新材料，只推断新增部分，增量写入。PRD 和草图也支持重新生成覆盖旧版本。
版本历史由 git 承担，不需要内置版本化。
PMContext 内部用显式标记区分确定性内容与风险内容：
`[待确认]` 标记材料完全缺失、Agent 无法推断的项，`[假设]` 标记 Agent 推断（置信度 < 8），`[冲突]` 标记矛盾。
View（PRD/草图）忠实反映这些标记，未确认项不能写成确定性要求。
追溯简化为"有来源 / 无来源"一级：每项内容要么行内标注来源（`← 来源: 项目扫描/知识库/对话/推断`），要么无来源。
无来源的项自动标 `[假设]`。不再区分 Strong/Weak Trace 二级——推断中产出的内容天然有定位。
_Avoid_: 原始材料的堆放（那是采集产物不是上下文）、不可追溯的会议纪要、单独的检查报告、Strong/Weak Trace 二级追溯、拆成多文件

**/pm-prd**:
user-invoked。从 PMContext 同时输出给 AI 和给人的两种 PRD 形态。
生成时确保每条需求都追溯到 PMContext 中的具体项，无来源的需求标 `[待确认]`。
内含 /pm-aiprd 和 /pm-humanprd 两个子步骤，也可单独调用。
_Avoid_: 跳过 PMContext 直接从聊天生成 PRD、需求项无追溯

**/pm-premortem**:
model-invoked。从 PMContext 假设上线失败，倒推风险并分类为 Tiger/Paper Tiger/Elephant，Tiger 按紧急度分为 Launch-Blocking/Fast-Follow/Track，为 Launch-Blocking Tiger 制定行动计划。与 PMContext 假设清单交叉检查，置信度 ≤ 5 的假设失败可能导致上线失败的升级为 Tiger。
产物写入 `docs/pm-context/premortem.md`，是 PMContext 的风险分析 View，和 PRD/草图平级。
_Avoid_: 脱离 PMContext 凭空列风险、风险项无追溯

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

**PM Thinking Loop（心智链）**:
LLM 内部的 6 步隐式推理协议（理解→建模→方案→权衡→风险→交付），不落盘，是每个 Skill 的思考纪律。
心智链约束的是 LLM 的**思考结构**——每步必须产出什么、下一步必须消费上一步的什么。不约束"怎么想"（那由现有行为纪律管），只约束"想出来的东西结构完整"。
与现有行为纪律正交：行为纪律管"怎么做"，心智链管"每步必须产出什么且必须消费上一步产出"。
_Avoid_: 把心智链写成"请仔细思考"的空话、把心智链当 Entity 或 View

**流程链（Process Chain）**:
心智链在现有 Skill 编排链上的显式切片落地，产出中间工件落盘到 `.loop/` 目录。
6 步不替换现有编排（collect→refine→审计门→prd→sketch），而是按 Skill 职责分工横切在上面。
_Avoid_: 把流程链当成新编排取代现有编排、在现有编排之外再跑一套并行流程

**Thinking Protocol**:
SKILL.md body 中的显式段，声明该 Skill 承载流程链的哪些步骤，及每步的产出约束和依赖检查。
格式：表格（步骤 | 本 Skill 的职责 | 产出是否回灌 PMContext）+ 执行纪律 + 审计三元组要求。
放置位置：Instructions 段之后，流程段之前。
_Avoid_: 写成"请仔细思考"的废话、不带产出约束的笼统描述

**中间工件（Intermediate Artifact）**:
流程链步骤产出的过程性工件，落盘到 `docs/pm-context/.loop/<skill>-step<N>.md`。
是 PMContext 的构建快照——不是 Entity（不被长期引用、不参与追溯主链路），PMContext 成熟后可清理。
_Avoid_: 把中间工件当 Entity、在 PMContext 或 View 中引用中间工件路径

**审计三元组（Audit Triple）**:
每步产出必备的全程追溯链，格式：`<依据集> → [工具/技术] → [转换操作] → <产出>`。
完整版写入 `.loop/` 中间工件，摘要（决策点+依据源数+工具名）回灌到 PMContext「决策日志」表。
**反同义反复红线**：转换操作必须阐明具体推导逻辑（同义词推导/多对多实体映射/边界隔离分析等），"将 A 转换为 A'"、"基于上述依据产出"、"经过分析得到"等空话判定为 Failure，由 darwin-skill dim8 检测兜底。
_Avoid_: 走形式的空三元组、不检查依赖就写三元组、"依据集"为空的三元组、同义反复的转换操作描述

**原子叠加（Atomic Stacking）**:
单个 Skill 内部跨 Step 的回灌在 LLM 上下文内做原子级叠加，不逐步 I/O 写 `pm-context.md`。仅在该 Skill 执行完毕（Model-Invoked Exit）时做单次批量落盘——避免 step 间反复读写 PMContext 引起的上下文切换与读写冲突。
_Avoid_: Skill 内每个 step 跑完就立刻 I/O 写 PMContext、把中间叠加状态泄露到对话上下文

**自愈机制（Self-Correction Loop）**:
依赖检查失败时，模型在隐式思考空间内立即触发回溯自愈——重新生成当前步骤产出直至通过依赖检查。最多 3 轮，超出仍失败则降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户。
_Avoid_: 依赖检查失败直接中止报错、把未通过校验的半成品直接落盘或回灌、自愈轮数无上限死循环

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

- **/pm-setup**（user-invoked）首次配置项目（含知识库路径），后续 Skill 自动读取。
- **/pm-need**（user-invoked）编排 **/pm-collect** 和 **/pm-refine**（model-invoked），全自动一次跑完，产出 PMContext 后停在审计门。支持 `--auto` 零确认模式：collect → refine → premortem → PRD → 原型一气呵成，PM 零介入。
- /pm-collect 和 /pm-refine 也可独立调用。
- **零确认模式**（--auto）：审计门不暂停，自动推进到 `/pm-premortem --auto` → `/pm-prd --auto` → `/pm-sketch --prototype --auto`，输出一站式报告。premortem 在 --auto 模式下强制编入主链路，作为流程链第 5 步（风险）的承载者。
- **正常模式**：审计门：PMContext 落盘后输出置信度分布 + 信息缺口，PM 决定通过/补充材料/修改。
- **/pm-prd**（user-invoked）编排 **/pm-aiprd** 和 **/pm-humanprd**（model-invoked）。支持 `--auto` 零确认、`--skip-ai`、`--skip-human`。
- /pm-aiprd 和 /pm-humanprd 也可独立调用。
- **/pm-premortem**（model-invoked）从 PMContext 假设失败并倒推风险，产出风险分析 View。--auto 模式下强制编入主链路（collect→refine→premortem→prd→sketch），正常模式可在 `/pm-prd` 之后或独立调用。
- **/pm-sketch**（user-invoked）编排 **/pm-wireframe**、**/pm-ia**、**/pm-state**、**/pm-flow**（model-invoked）。支持 `--prototype` 高质量 HTML 原型模式、`--auto` 零确认模式。
- 四个草图子 Skill 也可独立调用。
- **关联增强**：关联纪律分散进所有环节——collect 建材料间关联，refine 建事实/规则/页面/验收关联，prd 确保需求追溯到 PMContext，sketch 确保图元对应实体/关系。
- **心智链纪律**：PM Thinking Loop（6 步漏斗）横向嵌入每个 Skill 的 `## Thinking Protocol` 段，按 Skill 职责分配对应步骤。每步产出约束 + 依赖检查 + 审计三元组，确保推理链有结构、可审计。

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
| pm-setup | user-invoked | 首次使用 PMSkill 时配置项目（产物目录/语言/知识库路径/Agent 规则）。Run once before first use of the other PMSkill commands. |
| pm-need | user-invoked | 从模糊想法或用户诉求出发，全自动收集材料并推断澄清，沉淀成 PMContext，支持 --auto 零确认模式一键直达 PRD + 原型 |
| pm-collect | model-invoked | 主动深度扫描 URL、项目 docs/git/TODO/配置/目录结构、知识库和对话上下文，按材料类型聚合。Use when materials are needed before refining. |
| pm-refine | model-invoked | 对已收集材料自主推断澄清，标记事实/[假设]/[待确认]/[冲突]，沉淀成 PMContext。Use when collected materials exist and need clarification. |
| pm-prd | user-invoked | 从 PMContext 生成 PRD 文档（给 AI 和给人两种形态），支持 --auto 零确认模式 |
| pm-aiprd | model-invoked | 从 PMContext 生成给 AI 执行的 PRD，含可执行规则、数据模型、[待确认]分级处理。Use when another skill needs Agent-executable PRD. |
| pm-humanprd | model-invoked | 从 PMContext 生成给人阅读的 PRD，含决策理由和格式纪律。Use when the user asks for a human-readable PRD or review document. |
| pm-premortem | model-invoked | 从 PMContext 假设失败并倒推风险，产出 Tiger/Paper Tiger/Elephant + 紧急度分级 + 行动计划 + 假设交叉检查。Use when preparing for launch. |
| pm-sketch | user-invoked | 从 PMContext 生成全部草图（线框/信息架构/状态机/流程图）+ HTML 可交互原型。支持 --prototype/--auto |
| pm-wireframe | model-invoked | 从 PMContext 生成界面线框图。Use when the user asks for wireframe or page layout. |
| pm-ia | model-invoked | 从 PMContext 生成信息架构图。Use when the user asks for information architecture or entity relationships. |
| pm-state | model-invoked | 从 PMContext 生成状态机图。Use when the user asks for state machine or state transitions. |
| pm-flow | model-invoked | 从 PMContext 生成流程图。Use when the user asks for flowchart or process flow. |

user-invoked 设置 `disable-model-invocation: true`，description 人看一句话；model-invoked 不设置，description 带 "Use when..." trigger phrasing。

## SKILL.md Body 约定

user-invoked 编排入口极简：
- `/pm-need`：Run `/pm-collect` to gather materials, then run `/pm-refine` to infer and clarify, producing PMContext. Then output audit summary and wait for PM confirmation. If `--auto` flag, advance to `/pm-prd --auto` then `/pm-sketch --prototype --auto` without stopping.
- `/pm-prd`：Run `/pm-aiprd` and `/pm-humanprd` to produce both PRD forms from PMContext. If `--auto`, skip audit gate.
- `/pm-sketch`：Run `/pm-wireframe`, `/pm-ia`, `/pm-state`, and `/pm-flow` to produce all sketches from PMContext. If `--prototype`, also generate HTML interactive prototype.
- `/pm-setup`：流程已在上方定义（Explore → Ask → Write，Ask 含知识库路径）。

model-invoked Skill 的 body 包含完整纪律和流程（它们是可被独立调用的复用单元）。

每个 SKILL.md body 在 Instructions 段之后、流程段之前，新增 **## Thinking Protocol** 段，声明该 Skill 承载 PM Thinking Loop 的哪些步骤及每步的产出约束与依赖检查。格式详见 ADR 0008。

## Relationships

- **PM** 经过 **PM Thinking Loop**（隐式推理协议，不落盘）→ 驱动 **流程链**（在编排链上显式切片落地）→ 产出 **中间工件**（`.loop/`，构建快照，可丢弃）。
- **PM** 使用 **PMSkill** → 产出 **PMContext**（唯一 Entity）。
- **PMContext** 衍生出两类 **View**：**PRD** 和 **草图**。
- **PRD** 有两种形态：给 AI 的、给人的。
- **草图** 有多种形态：界面线框、信息架构图、状态机、流程图等。
- 所有 View 必须可追溯到 **PMContext**，不可凭空生成。
- **流程链** 的中间工件中，达阈值的关键信息自动回灌 **PMContext** 现有 heading，不开新 heading、不走新标记体系。
- **审计三元组**（`<依据集 → 工具/技术 → 产出>`）完整版落 `.loop/`，摘要回灌 PMContext「决策日志」表。

## 产物目录布局

```
docs/pm-context/
  pm-context.md          ← Entity（唯一）
  collect/               ← /pm-collect 整理后的材料
  .loop/                 ← 流程链中间工件（构建快照，PMContext 成熟后可清理）
    collect-step1.md     ← /pm-collect 问题重构
    refine-step2.md      ← /pm-refine 领域模型片段
    refine-step3.md      ← /pm-refine 方案候选
    refine-step4.md      ← /pm-refine 决策表
    premortem-step5.md   ← /pm-premortem 风险清单
  prd/                   ← PRD View
    ai-prd.md            ← /pm-aiprd 产物
    human-prd.md         ← /pm-humanprd 产物
  premortem.md           ← /pm-premortem 产物（风险分析 View）
  sketch/                ← 草图 View
    prototype.html       ← /pm-sketch --prototype 产出的 HTML 可交互原型
    wireframe.md
    ia.md
    state.md
    flow.md
```

## Flagged Ambiguities

- "采集/精炼/关联/生成"四阶段是旧项目概念，仅作参考，已被 PMContext 主链路取代。
- "草图"不等于"PRD 的配图"——它是独立 View，和 PRD 平级。
- Soft Gate / 独立检查机制已去掉，改为 PMContext 内显式标记（[待确认]/[假设]/[冲突]），View 忠实反映。
- 1by1 追问机制已去掉，改为 Agent 自主推断 + 审计门。PM 唯一介入点是审计 PMContext。
- 知识库是可选外部材料源，不替代项目扫描和对话上下文，三者互补。
- 零确认模式（--auto）跳过审计门但不跳过置信度标记——输出的一站式报告仍包含完整的置信度分布，PM 事后审计。
- HTML 原型（prototype.html）是草图的增强形态，和 Mermaid 草图平级，不替代 Mermaid。前者适合用户预览交互效果，后者适合 Agent 阅读和编辑。
- 项目深扫描是 pm-collect 的核心增值点——扫描结果纳入 PMContext 推断，使 Agent 能自主发现项目中的约束和已知问题，无需 PM 手动描述。
- **心智链 vs 流程链**：心智链（6 步隐式推理，不落盘）约束 LLM 的思考结构；流程链（6 步在编排链上的显式切片，落盘 `.loop/`）约束每步的产出与依赖。两层正交，互不替代。心智链是引擎，流程链是管道。
- **中间工件不是 Entity**：`.loop/` 下的文件是 PMContext 的构建快照，有身份可被引用，但可清理、不参与追溯主链路、不是永久领域概念。PMContext 仍是唯一 Entity（ADR 0004 不变）。
- **回灌约束**：流程链中间工件中达阈值的关键信息自动回灌 PMContext 现有 heading，不开新 heading、不走新标记体系、来源标注 `← 来源: loop step N`。回灌走 LLM 自主判断，阈值不清晰时可依赖 darwin-skill 的实测验证来检测过度回灌/欠回灌。
- **审计三元组不是追溯替代**：审计三元组（`<依据集 → 工具/技术 → 产出>`）是流程链的审计手段，完整版落 `.loop/`，摘要回灌决策日志。它补充但不替代现有 PMContext 的一级追溯（有来源/无来源），后者仍然是 View 的唯一追溯依据。
- **回灌原子性**：Skill 内跨 Step 回灌在 LLM 上下文内做原子级叠加，仅 Model-Invoked Exit 时单次批量落盘 PMContext。避免 step 间反复 I/O 引起上下文切换与读写冲突。
- **依赖检查失败处置**：不中止、不裸奔落盘，必须触发隐式自愈重生成（最多 3 轮）。超限降级为 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户。
- **`.loop/` GC 策略已锁定**：默认写入 `.gitignore`；每次 `/pm-need <需求描述>` 入口调用时自动 Wipe 全量清空；`--incremental` 模式例外不清空。
- **反同义反复红线**：审计三元组的转换操作必须阐明具体推导逻辑（同义词推导/多对多实体映射/边界隔离分析等），空话判定为 Failure，darwin-skill dim8 检测兜底。
