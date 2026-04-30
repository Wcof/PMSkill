# PRD Context Skill Kit - 项目说明

## 项目定位

PRD Context Skill Kit 是 PRD helper 的第一版 MVP / Demo。

它是一个通用 Agent Skill 套件，用于验证产品经理能否通过"采集 → 精炼 → 关联 → 生成 → 检查"流程，把原始沟通和原型信息转化为可追溯、可复用、可被 Agent 使用的结构化产品上下文。

## 核心问题

AI 辅助开发中的主要瓶颈不是更好的 prompt，而是上下文。Claude Code、Codex、Cursor、Trae 等 Agent 缺少项目真实背景、组织知识、历史决策和业务规则时，容易局部优化、误解需求或生成无法落地的代码。

## 解决方案

通过四个业务模块加一个横向质量机制，建立从原始沟通到结构化 PRD 的处理链路：

```
采集（collect）→ 精炼（refine）→ 关联（relate）→ 生成（generate）
                    ↕              ↕              ↕              ↕
                  检查            检查            检查            检查
```

## 四个业务模块

| 模块 | 目标 | 输出目录 |
|------|------|---------|
| 采集 | 保存原始上下文，不让信息丢失 | 01-sources/ |
| 精炼 | 提取事实、决策、约束、冲突、问题 | 02-refined/ |
| 关联 | 建立需求→页面→规则→数据→验收关系 | 03-relations/ |
| 生成 | 输出角色化 PRD 和 Agent 上下文 | 04-generated/ |

## 检查机制

检查不是第五个业务模块，而是贯穿四个模块的质量门禁。每一步都必须输出 `check.md`。

## Context Delta

每次完成任务后，必须输出 Context Delta，记录本轮上下文增量，防止 Agent 对话中的新信息丢失。

## 不做什么

第一版不做：网页 UI、后台系统、数据库、登录注册、权限系统、完整多项目管理、知识图谱、自动 Axure/Figma 解析、商业化 SaaS、团队协同平台。

## 支持工具

- Claude Code
- Codex
- Trae
- 通用 Agent
