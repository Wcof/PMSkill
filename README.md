# PRD Helper

[中文](README.md) | [English](README.en.md)

![PRD Helper 项目介绍图](support/assets/prd-helper-project-overview.svg)

## 一句话价值

PRD Helper 把分散在会议、聊天、评审和旧文档里的产品上下文，沉淀成可追溯、可检查、可复用的结构化 PRD 资产。

## 它解决什么问题

很多团队不是没有需求资料，而是资料散、来源乱、版本多，最后 PRD 变成“谁记得就听谁的”。PRD Helper 的目标是让 Agent 和团队先保存原始材料，再精炼信息、建立关系，最后生成 PRD，避免直接让 AI 从碎片聊天里凭感觉写文档。

## 核心功能

| 功能 | 用处 | 解决的问题 |
|---|---|---|
| 项目初始化 `/prd-helper` | 创建配置、目录和后续命令 | 安装后项目还不能直接用 |
| 主动采集 `/prd-start` | 开始记录后续产品讨论 | 关键会话容易遗漏 |
| 暂停/恢复/停止采集 | 控制采集边界并清理 Hook | 采集范围不清、误采集 |
| 批量扫描 `/prd-scan` | 导入历史 Agent 会话 | 旧上下文无法进入流程 |
| 被动材料目录 | 手动放入会议纪要、旧 PRD、客户反馈 | 非聊天材料无法统一管理 |
| 四模块流程 | Collect -> Refine -> Relate -> Generate | 直接生成 PRD 容易漏项和幻觉 |
| 检查脚本 | 每个阶段都能被验证 | 产物不可审计 |
| Grill 模式 `/prd-grill` | 质询模糊概念和冲突点 | 术语不清、决策没沉淀 |
| 卸载 `/prd-remove` | 清理命令、配置和 Hook | 项目被安装残留污染 |

## 快速开始

### 1. 安装 Skill

```bash
npx skills@latest add Wcof/PRDContextEngine
```

安装器里用 `↑/↓` 移动，`Space` 勾选，`Enter` 确认。选择 `prd-helper`，并选择你要安装到的 Agent，例如 Claude Code 或 Codex。

### 2. 初始化当前项目

在 Agent 会话中输入：

```text
/prd-helper
```

初始化会创建默认目录 `docs/prd-helper/`，并生成后续命令。

### 3. 使用采集命令

```text
/prd-start   # 开启主动采集，开始记录产品讨论
/prd-pause   # 暂停主动采集，临时停止记录并清理 Hook
/prd-resume  # 恢复主动采集，继续记录
/prd-stop    # 停止采集，生成采集摘要和检查结果
/prd-status  # 查看当前采集状态
/prd-scan    # 扫描历史 Agent 会话并导入采集池
/prd-grill   # 进入压力测试模式，挑战矛盾和模糊点
/prd-remove  # 卸载 PRD Helper 并清理项目配置
```

主动采集内容会进入：

```text
docs/prd-helper/01-collect/active/
```

手动材料放入：

```text
docs/prd-helper/01-collect/passive/
```

## 四模块工作流

| 模块 | 目录 | 产物目标 |
|---|---|---|
| Collect 采集 | `modules/collect/` | 保存原始材料、建立索引、轻量标记噪音 |
| Refine 精炼 | `modules/refine/` | 提炼事实、决策、约束、问题、推断 |
| Relate 关联 | `modules/relate/` | 建立事实、页面、规则、数据、验收之间的关系 |
| Generate 生成 | `modules/generate/` | 生成给产品、研发、测试使用的 PRD 上下文 |

## 检查命令

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

## 常见问题

只看到 `/prd-helper`，没有 `/prd-start`：先执行一次 `/prd-helper` 完成项目初始化。Claude Code 有时需要重开会话刷新命令列表。

采集没有写入：先运行 `/prd-status`，确认状态是 `on`；再检查 `docs/prd-helper/01-collect/collect-state.md`。

不想继续使用：运行 `/prd-remove`，它会清理项目配置、命令和 Hook，但默认保留已经生成的 `docs/prd-helper/` 文档。

## 开源协作

- 贡献指南：`CONTRIBUTING.md`
- 行为准则：`CODE_OF_CONDUCT.md`
- 安全策略：`SECURITY.md`
- 支持方式：`SUPPORT.md`
- 版本记录：`CHANGELOG.md`
- GitHub 介绍图 Prompt 指南：`docs/github-project-kit.md`
