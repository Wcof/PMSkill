# PRD Helper Context

PRD Helper 把分散的产品上下文沉淀为可追溯、可检查、可复用的结构化 PRD 资产。本文档定义项目自己的领域语言，帮助 Agent 在采集、精炼、关联、生成四阶段中使用一致术语。

## Language

**PRD Helper Skill**:
单一 Agent Skill，负责组织采集、精炼、关联、生成四阶段工作流。
_Avoid_: skill collection, 多个业务 skill

**PRD Context Compiler（PRD 上下文编译流程）**:
把原始产品上下文经过采集、精炼、关联、检查后，编译成可追溯的 PRD 文档和指导人或 Agent 实施的工程上下文。Agent 负责语义转换，脚本负责结构、链路、来源和风险门禁。
_Avoid_: 自动 PRD 写作器、无来源生成器

**Collect（采集）**:
保存原始材料、元信息、索引、状态和轻量摘要的阶段。
_Avoid_: 清洗、总结成 PRD、事实提取

**Refine（精炼）**:
从采集材料中提取事实、背景、目标、决策、约束、冲突、问题和 AI 推断的阶段。
_Avoid_: 生成规则、生成 PRD、建立完整关系链

**Relate（关联）**:
建立事实、页面、功能、规则、数据、验收之间关系链路的阶段。
_Avoid_: 画图而不检查断链、孤立项

**Generate（生成）**:
基于精炼与关联结果输出 PRD 文档和 Agent 上下文的阶段。
_Avoid_: 从原始材料直接生成、凭空补业务规则

**Limited Generate（受限生成）**:
`/prd-generate` 永远可以执行；但当前置产物缺失或 Check 未通过时，生成结果不是完整确定性 PRD。受限生成必须显式标记缺失来源、断链、待确认问题和禁止实施项，不能把未来源化或未关联内容写成确定性要求。
_Avoid_: 静默补齐、伪装成完整 PRD、把风险项写成实施项

**检查（Check） / Soft Gate（软门禁）**:
贯穿各阶段的软门禁，不是第五个业务阶段。Check 默认不阻断用户继续执行命令，但必须暴露来源缺失、断链、结构缺口和待确认风险；未通过内容只能进入风险或待确认区，不能写成确定性 PRD 或 Agent Context 要求。
_Avoid_: 第五模块、独立业务阶段、硬阻断

**Active Capture（主动采集）**:
`/prd-start` 后记录完整 `User Query + Agent Answer` 的采集方式。
_Avoid_: 默认常开采集、只在回复中声称已记录

**Passive Source（被动材料）**:
用户放入 `docs/prd-helper/01-collect/passive/` 或通过 `/prd-import` 导入的原始材料。
_Avoid_: 被 Agent 改写后的材料

**Source Index（材料索引）**:
`source-index.md`，记录来源、路径、hash、通道、元信息状态和采集状态。
_Avoid_: 摘要表、事实表

**Traceability（可追溯性）**:
最低标准不是只有来源文件，而是有可定位来源锚点。来源锚点至少包括 `source_id + path + quote/paraphrase + locator`；`locator` 可以是行号、段落标题、turn 编号、时间戳或消息序号。
_Avoid_: 只写“来源：会议”或“来源：meeting.md”

**Strong Trace（强追溯）**:
具备完整来源锚点，复核者可以回到原始材料定位上下文。强追溯内容才可以进入确定性 PRD 或 Agent Context 要求。
_Avoid_: 只有来源文件、没有定位信息

**Weak Trace（弱追溯）**:
只有来源文件或笼统来源说明，缺少可定位 `locator`。弱追溯内容只能进入风险或待确认区，不能写成确定性要求。
_Avoid_: 当成已确认事实或实施项

**Collect State（采集状态）**:
`collect-state.md`，记录采集 session、capture mode、计数、最近写入和研讨状态。
_Avoid_: Agent 口头记忆

**Fact（事实）**:
来源中明确出现、可追溯、可引用的需求事实。
_Avoid_: assumption, suggestion

**Assumption（推断）**:
Agent 基于来源做出的不确定判断，必须说明依据和不能确定的原因。
_Avoid_: fact

**Conflict（冲突）**:
不同来源、角色或陈述之间尚未统一的矛盾。
_Avoid_: question

**Question（待确认问题）**:
需要用户、产品、业务或团队继续确认的问题。
_Avoid_: 已确认事实

**Relation Chain（关系链路）**:
从事实连接到页面/功能、规则、数据和验收的上下游链路。
_Avoid_: 只列实体、不连关系

**Agent Context（Agent 上下文）**:
生成阶段输出给前端、后端、测试、产品复核和执行 Agent 使用的任务上下文。
它是指导人或 Agent 实施的工程上下文，不只是 PRD 附属物。
_Avoid_: 新的事实来源、普通摘要

**View（视图文档）**:
生成阶段的文档文件是对已有事实、关系、规则、数据、验收和风险的视图，不是新的事实来源，也不是新的领域实体。
_Avoid_: 把 overview/page-prd/rule-prd/agent-context 文件类型当成业务实体

**Entity（领域实体）**:
只有跨阶段流转、需要被引用、需要 ID、需要参与关系链路的对象，才是领域实体。
_Avoid_: 因为某类文档有文件或模板就把它升级成实体

**PRD Discuss（需求研讨）**:
`/prd-discuss`，用于追问矛盾、模糊术语和未决问题的辅助模式。
_Avoid_: 第五阶段、替代精炼

**Atomic Command（原子指令）**:
每个斜杠命令只对应一个明确操作，如初始化、开始、停止、扫描、导入、精炼、关联、生成、研讨、卸载。
_Avoid_: `/prd-helper start`, `/prd-setup`, 包装命令

## Relationships

- **PRD Helper Skill** 包含四个业务阶段：**Collect**、**Refine**、**Relate**、**Generate**。
- **Check** 验证每个阶段产物并输出软门禁风险，但不改变四阶段模型，也不默认阻断用户继续执行。
- **Collect** 产生 **Source Index** 和 **Collect State**，并保存 **Active Capture** 与 **Passive Source**。
- **Refine** 读取采集材料，产生 **Fact**、**Assumption**、**Conflict**、**Question** 等结构化上下文，并区分 **Strong Trace** 与 **Weak Trace**。
- **Relate** 把 **Fact** 连接到页面/功能、规则、数据和验收，形成 **Relation Chain**。
- **Generate** 读取精炼与关联产物，输出 PRD 文档和 **Agent Context**；当前置产物缺失或 Check 未通过时，只能进入 **Limited Generate**。
- **Agent Context** 是给人或 Agent 执行实施的指导性文件，必须保留来源、断链和待确认风险，不能把缺失来源或断链内容写成确定性要求。
- **Generate** 产物中的文档文件是 **View**，不是新的 **Entity**；只有跨阶段流转、需要 ID 和关系链路的对象才是实体。
- **PRD Discuss** 辅助发现和澄清问题，结论必须回流到 **Refine** 产物或本文档。

## Example Dialogue

> **User:** “把这些会议纪要直接生成一份 PRD。”
>
> **Agent:** “我会先进入 **Collect（采集）** 保存原文，再做 **Refine（精炼）** 区分事实、冲突和待确认问题，然后通过 **Relate（关联）** 建立事实到页面、规则、数据、验收的链路。只有这些产物可追溯后，才进入 **Generate（生成）**。”

## Flagged Ambiguities

- “清洗材料”容易被误解为改写原文。当前约定：采集阶段不清洗原文，只索引和标记元信息；精炼阶段才分类信息。
- “讨论/研讨”容易被误解为第五阶段。当前约定：`/prd-discuss` 是辅助模式，结论必须回到精炼产物或 `CONTEXT.md`。
- “生成 PRD”容易被误解为可以直接从聊天生成。当前约定：生成必须基于 `02-refine/` 和 `03-relate/`。
- “规则”可能被误写进精炼阶段。当前约定：精炼记录事实、决策和约束；规则链路在关联阶段建立，规则文档在生成阶段输出。
