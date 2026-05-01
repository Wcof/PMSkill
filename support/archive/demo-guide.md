# PRD Helper Skill Kit Demo 演示指南

## 5 分钟讲清楚背景

### 问题

AI 辅助开发中的主要瓶颈不是更好的 prompt，而是上下文。

Claude Code、Codex、Cursor、Trae 等 Agent 缺少项目真实背景、组织知识、历史决策和业务规则时，容易局部优化、误解需求或生成无法落地的代码。

多 Agent 协作时，如果没有共享上下文和增量记录，每个 Agent 都会从零开始。

### 解决方案

PRD Helper Skill Kit 是一个通用 Agent Skill 套件，通过"采集 → 精炼 → 关联 → 生成 → 检查"流程，把原始沟通和原型信息转化为可追溯、可复用、可被 Agent 使用的结构化产品上下文。

### 核心价值

1. **不让原始上下文丢失**：采集环节保存所有原始材料
2. **区分事实和推断**：精炼环节明确标记 AI 推断
3. **不让需求断链**：关联环节建立需求→页面→规则→数据→验收关系
4. **角色化输出**：生成环节为不同角色生成不同上下文
5. **质量门禁**：检查机制贯穿每一步

---

## 10 分钟演示完整流程

### 第一步：展示原始材料（1 分钟）

打开 `examples/robot-inspection/docs/prd-helper/01-collect/` 目录。

说明：

> 这是机器人巡检场景产生的原始信息。它包含产品口述、会议纪要、原型说明、Agent 对话摘要和客户反馈。这些内容原本会散落在聊天、会议、原型和 Agent 对话里。

展示文件：
- `product-voice.md` - 产品口述
- `meeting-notes.md` - 会议纪要
- `prototype-notes.md` - 原型说明
- `agent-session.md` - Agent 对话摘要
- `customer-feedback.md` - 客户反馈

### 第二步：展示采集检查（1 分钟）

打开 `01-collect/check.md`。

说明：

> PRD Helper Skill 先不急着写 PRD，而是把原始上下文保存下来，并检查是否完整。

展示检查项：来源、类型、时间、涉及模块、未改写。

### 第三步：展示精炼结果（2 分钟）

打开 `02-refine/` 目录。

说明：

> 系统从原始材料中提取需求事实、业务背景、业务目标、设计决策、业务约束、冲突点和待确认问题。

展示文件：
- `facts.md` - 12 条需求事实，每条有来源和可信度
- `background.md` - 业务背景
- `goals.md` - 业务目标
- `decisions.md` - 5 条设计决策
- `constraints.md` - 6 条业务约束
- `conflicts.md` - 1 条冲突（待确认）
- `questions.md` - 4 条待确认问题
- `assumptions.md` - 7 条 AI 推断（标记为待确认）

重点展示：事实和推断的区分。

### 第四步：展示关联结果（2 分钟）

打开 `03-relate/` 目录。

说明：

> 系统把需求事实关联到页面、功能、规则、数据和验收标准。这一步是普通 PRD 生成器没有的能力。

展示文件：
- `page-map.md` - 需求→页面关联（8 个页面）
- `feature-map.md` - 功能→规则关联（8 个功能）
- `rule-map.md` - 规则→数据关联（8 条规则）
- `data-map.md` - 数据对象关系（9 个对象）
- `acceptance-map.md` - 验收关联（6 个验收项）
- `context-map.md` - 上下文总关联

重点展示：无孤立对象、无断链。

### 第五步：展示生成结果（2 分钟）

打开 `04-generate/` 目录。

说明：

> 系统生成不同角色可用的文档：产品看项目说明和决策记录；前端看页面说明；后端看功能规则和数据说明；测试看验收标准；Agent 看压缩后的执行上下文。

展示文件：
- `overview/project-overview.md` - 项目说明
- `pages/inspection-point-management.md` - 页面说明
- `rules/inspection-point-rule.md` - 业务规则
- `data/inspection-domain-data.md` - 数据说明
- `acceptance/inspection-point-acceptance.md` - 验收标准
- `agent-context/` - 四份 Agent 上下文

### 第六步：展示检查结果（1 分钟）

打开 `05-check/` 目录。

说明：

> 系统检查是否存在断链、遗漏、冲突和无来源推断，并输出 Context Delta。

展示文件：
- `full-check.md` - 整体完整性
- `gap-check.md` - 缺口分析
- `relation-check.md` - 关系完整性
- `source-check.md` - 来源追溯
- `generated-check.md` - 生成质量
- `context-delta.md` - 本轮增量

### 第七步：总结价值（1 分钟）

说明：

> 这个 Demo 证明：PRD helper 不是单纯生成 PRD，而是把原始沟通到 Agent 执行之间的上下文链路串起来。

总结要点：
1. 完整闭环：采集→精炼→关联→生成，检查贯穿全流程
2. 事实推断分离：AI 推断不会被当成事实
3. 关系完整：无孤立对象、无断链
4. 角色化输出：不同角色看不同上下文
5. 增量记录：Context Delta 防止信息丢失

---

## 这个 Demo 解决了什么问题

1. **上下文丢失**：采集环节保存所有原始材料
2. **事实推断混淆**：精炼环节明确区分
3. **需求断链**：关联环节建立完整关系
4. **角色割裂**：生成环节为不同角色生成不同上下文
5. **质量不可控**：检查机制贯穿每一步

## 下一版继续做什么

| 版本 | 方向 |
|------|------|
| v0.2 | 命令自动化脚本，增强结构检查 |
| v0.3 | 读取本地项目路由和页面文件 |
| v0.4 | 从 Axure/Figma 导入页面说明 |
| v0.5 | Agent Context 自动分发 |
| v1.0 | 轻量网页 Demo 或桌面工具 |
