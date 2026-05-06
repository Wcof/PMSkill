# PRD Helper Context

## Domain Vocabulary

- **PRD Helper Skill**: 一个单独的 Agent Skill，负责把原始产品上下文转成可追溯的 PRD 上下文资产。
- **Collect**: 采集模块，保存原始材料、元信息、索引、状态和轻量摘要。
- **Refine**: 精炼模块，从采集材料中提取事实、背景、目标、决策、约束、冲突、问题和 AI 推断。
- **Relate**: 关联模块，建立事实、页面、功能、规则、数据、验收之间的关系。
- **Generate**: 生成模块，输出项目说明、页面说明、规则说明、数据说明、验收标准和 Agent 上下文。
- **Check**: 横向质量门禁，不是第五个业务模块。
- **Active Capture**: Agent 在 `/prd-start` 后主动记录完整 User Query + Agent Answer。
- **PRD Grill**: `/prd-grill`，在 Active Capture 基础上开启持续质询模式。扫描已采集材料找矛盾，逐个问题压力测试产品方案，实时更新 CONTEXT.md，按需创建 ADR。
- **Grill Mode**: `collect-state.md` 中的 `grill_mode` 字段，`on` 表示 grill 进行中，`off` 表示未激活或已结束。
- **Batch Scan**: `/prd-scan`，扫描当前项目在所有 AI 编码工具（Claude Code、Cursor、Trae、Codex）中的历史 session 并批量采集。可独立运行，不依赖 `/prd-start`。
- **Passive Source**: 用户放入 `docs/prd-helper/01-collect/passive/` 的原始材料。
- **Source Index**: `source-index.md`，记录材料来源、路径、hash、通道和状态。
- **Collect State**: `collect-state.md`，记录采集 session 状态和增量写入检查点。
- **原子指令**: 每个斜杠命令对应 Skill 生命周期的一个离散状态操作（初始化、开始、暂停、恢复、停止、查状态、卸载），不包装、不分发。
_Avoid_: 包装命令、兼容入口、总入口
- **Skill 名称**: `prd-helper`，是安装标识（npm/skills 安装时使用），与命令命名解耦。
- **命令集合**: `/prd-helper`、`/prd-start`、`/prd-stop`、`/prd-status`、`/prd-scan`、`/prd-grill`、`/prd-remove`。
_Avoid_: `/prd-helper start`、`/prd-setup`
- **实体生命周期**: 一个实体类型从 Collect/Refine/Relate/Generate 中哪些模块经过、每个模块对它做什么；静态定义由 `scripts/lib/id_registry.py` 的 `EntityType.lifecycle` 描述。

## Architecture Language

- 根目录 `SKILL.md` 是唯一 Skill 入口。
- `modules/*` 是同一个 Skill 内部的业务模块。
- `scripts/lib/*` 是脚本共享库，状态、索引、时间、哈希、模板解析等公共逻辑必须放在这里。
- `scripts/lib/constants.py` 是路径、命令和生成结构等静态配置的唯一位置；行为逻辑不要放在常量模块里。
- `support/adapters/canonical-rules.md` 是适配器共性规则的来源。
