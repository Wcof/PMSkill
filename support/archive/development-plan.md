# PRD Helper Skill Kit 开发计划

## 版本路线图

### v0.1（当前版本）

**目标**：通用 Skill + Markdown 工作流，跑通四环节完整闭环。

**交付物**：
- 通用 Skill 目录结构
- SKILL.md 主入口
- 四环节工作流（采集、精炼、关联、生成）
- 检查规则和脚本
- 26 个模板文件
- 4 类工具适配（Codex、Claude Code、Trae、Generic）
- 机器人巡检 Demo
- 完整检查套件

**状态**：已完成

---

### v0.2

**目标**：增加命令自动化脚本，增强结构检查。

**计划内容**：
- 开发 CLI 工具，支持一键执行采集、精炼、关联、生成、检查
- 增强 check-structure.py，支持更细粒度的检查
- 增强 check-relations.py，支持自动修复孤立对象
- 增强 check-generated.py，支持自动标记 TODO
- 支持增量处理，避免重复处理已有内容

**预计时间**：待定

---

### v0.3

**目标**：支持读取本地项目路由和页面文件。

**计划内容**：
- 自动扫描项目中的路由文件
- 自动提取页面组件信息
- 自动关联路由和页面
- 支持 React/Vue/Next.js 等主流框架

**预计时间**：待定

---

### v0.4

**目标**：支持从 Axure/Figma 导入页面说明。

**计划内容**：
- 支持从 Axure HTML 导出中提取页面信息
- 支持从 Figma API 获取页面结构
- 自动生成页面说明文档
- 自动关联原型和需求

**预计时间**：待定

---

### v0.5

**目标**：支持 Agent Context 自动分发。

**计划内容**：
- 自动为不同 Agent 生成上下文
- 支持上下文版本管理
- 支持上下文增量更新
- 支持多 Agent 协作时的上下文同步

**预计时间**：待定

---

### v1.0

**目标**：考虑做轻量网页 Demo 或桌面工具。

**计划内容**：
- 轻量网页界面
- 可视化上下文关系图
- 交互式确认流程
- 团队协作支持

**预计时间**：待定

---

## 当前版本详细计划

### 阶段一：建立通用 Skill 骨架

**交付物**：
- README.md
- repository root/SKILL.md
- repository root/references/
- repository root/modules/*/templates/
- repository root/scripts/

**验收标准**：
- 符合通用 Skill 目录结构
- SKILL.md 有 name 和 description
- SKILL.md 保持轻量
- 详细规则拆到 references
- 模板拆到 modules/*/templates

**状态**：已完成

---

### 阶段二：建立四环节模板

**交付物**：
- 26 个模板文件

**验收标准**：
- 每个模板有来源字段
- 每个模板有状态字段
- 每个模板有待确认字段
- 每个模板能支持检查

**状态**：已完成

---

### 阶段三：建立检查规则

**交付物**：
- references/check-rules.md
- scripts/check-structure.py
- scripts/check-relations.py
- scripts/check-generated.py

**验收标准**：
- 每一步都有 check.md 生成要求
- 最终有 05-check
- 脚本能检查目录和关键文件
- 脚本能输出缺失项

**状态**：已完成

---

### 阶段四：建立工具适配层

**交付物**：
- adapters/codex/
- adapters/claude-code/
- adapters/trae/
- adapters/generic/

**验收标准**：
- Codex 有 AGENTS.md 适配说明
- Claude Code 有 CLAUDE.md 适配说明
- Trae 有 Rules & Skills 适配说明
- Generic 可以复制粘贴使用

**状态**：已完成

---

### 阶段五：跑通机器人巡检 Demo

**交付物**：
- examples/robot-inspection/docs/prd-helper/

**验收标准**：
- 有 01-collect
- 有 02-refine
- 有 03-relate
- 有 04-generate
- 有 05-check
- 每个目录都有真实内容
- 能看出上下文从原始材料演化到生成文档
- 能看出检查发现了什么问题

**状态**：已完成

---

### 阶段六：整理 Demo 说明

**交付物**：
- docs/demo-guide.md
- docs/acceptance.md
- docs/development-plan.md

**验收标准**：
- 能用 5 分钟讲清楚 Demo 背景
- 能用 10 分钟演示完整流程
- 能说明这个 Demo 解决了什么问题
- 能说明下一版继续做什么

**状态**：已完成
