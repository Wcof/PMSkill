# PRD Context Skill Kit 验收标准

## 第一版成功标准

> 这个 Skill Kit 能不能在没有 UI、没有后台、没有数据库的情况下，跑通 PRD helper 自身产品上下文的完整闭环。

## 必须满足的条件

### 结构验收

| # | 验收项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 符合通用 Skill 结构 | ✅ | skills/prd-context/ 目录结构完整 |
| 2 | SKILL.md 有 name 和 description | ✅ | 有 frontmatter 定义 |
| 3 | SKILL.md 保持轻量 | ✅ | 详细规则拆到 references/ |
| 4 | 详细规则拆到 references/ | ✅ | 4 个参考文件 |
| 5 | 模板拆到 assets/templates/ | ✅ | 14 个模板文件 |

### 功能验收

| # | 验收项 | 状态 | 说明 |
|---|--------|------|------|
| 6 | 有采集模块 | ✅ | collect 流程和模板 |
| 7 | 有精炼模块 | ✅ | refine 流程和模板 |
| 8 | 有关联模块 | ✅ | relate 流程和模板 |
| 9 | 有生成模块 | ✅ | generate 流程和模板 |
| 10 | 每个模块都有检查 | ✅ | 每步输出 check.md |
| 11 | 最终有 05-check | ✅ | 完整检查套件 |
| 12 | 最终有 Context Delta | ✅ | context-delta.md |

### 适配验收

| # | 验收项 | 状态 | 说明 |
|---|--------|------|------|
| 13 | 能被 Codex 适配 | ✅ | adapters/codex/ |
| 14 | 能被 Claude Code 适配 | ✅ | adapters/claude-code/ |
| 15 | 能被 Trae 适配 | ✅ | adapters/trae/ |
| 16 | 通用 Agent 可复制使用 | ✅ | adapters/generic/ |

### 示例验收

| # | 验收项 | 状态 | 说明 |
|---|--------|------|------|
| 17 | 有真实示例 | ✅ | demo/prd-helper-demo/ |
| 18 | 示例主角是 PRD helper 自身 | ✅ | 自举示例 |
| 19 | 示例跑通完整闭环 | ✅ | 采集→精炼→关联→生成→检查 |

### 工具验收

| # | 验收项 | 状态 | 说明 |
|---|--------|------|------|
| 20 | 有模板文件 | ✅ | 14 个模板 |
| 21 | 有最小检查脚本 | ✅ | 3 个 Python 脚本 |

## 不验收的内容

以下内容不在第一版验收范围内：

- 网页 UI
- 后台系统
- 数据库
- 登录注册
- 权限系统
- 自动 Axure/Figma 解析
- 商业化 SaaS

## 验收结论

PRD Context Skill Kit 第一版验收通过。

核心验证目标已达成：在没有 UI、没有后台、没有数据库的情况下，跑通了 PRD helper 自身产品上下文的完整闭环。
