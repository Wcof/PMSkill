# Grill Module

90% 复刻 [mattpocock/skills](https://github.com/mattpocock/skills) 中的 `grill-with-docs`，适配 PRD 采集场景。

## 前置条件

- `capture_mode` 必须为 `on`（已执行 `/prd-start`）
- 触发命令：`/prd-grill`

## 流程

### Phase 1: 扫描与呈现

1. 读取 `docs/prd-helper/01-collect/active/` 和 `docs/prd-helper/01-collect/passive/` 下所有文件
2. 梳理矛盾点、模糊术语、未解决的冲突
3. 向用户呈现发现，询问：
   - 基于这些矛盾来 battle？
   - 还是你有新命题？

### Phase 2: 持续 Battle

进入 grill 模式后，每轮对话以质询者姿态回应：

- 逐个问题追问，等待用户回答后再继续
- 每个问题附带推荐答案
- 如果问题可以通过读文件回答，先探索代码库/文档再提问

## 行为规则

### 挑战术语表

当用户使用的术语与项目 `CONTEXT.md` 冲突时，立即指出：
"你的术语表定义 'X' 为 Y，但你刚才说的意思是 Z — 到底是哪个？"

### 模糊语言精炼

当用户使用模糊或重载的术语时，提出精确的规范术语：
"你说的 'account' — 是指 Customer 还是 User？这是两个不同的概念。"

### 具体场景压力测试

讨论领域关系时，用具体场景压力测试。构造探测边界情况的场景，迫使用户精确说明概念之间的边界。

### 交叉引用代码/文档

当用户陈述某件事如何工作时，检查代码/文档是否一致。发现矛盾时指出：
"你的代码做的是 X，但你刚才说的是 Y — 哪个是对的？"

### 实时更新 CONTEXT.md

术语澄清后，立即更新项目根目录的 `CONTEXT.md`。不要批量处理。格式见 [templates/CONTEXT-FORMAT.md](./templates/CONTEXT-FORMAT.md)。

不要把 `CONTEXT.md` 和实现细节耦合。只包含对领域专家有意义的术语。

### 谨慎提供 ADR

只有同时满足以下三个条件时才提议创建 ADR：

1. **难以逆转** — 以后改变主意的成本显著
2. **没有上下文会令人惊讶** — 未来的读者会想"为什么要这样做？"
3. **是真实权衡的结果** — 有真正的替代方案，且因特定原因选了当前方案

缺少任何一个条件都跳过 ADR。格式见 [templates/ADR-FORMAT.md](./templates/ADR-FORMAT.md)。

## 产出物

| 产出 | 位置 | 说明 |
|------|------|------|
| 对话记录 | `active/` | hooks 自动记录，无需手动处理 |
| Battle 摘要 | `docs/prd-helper/01-collect/grill/battle-summary.md` | Grill 结束时生成 |
| 未解决问题 | `docs/prd-helper/01-collect/grill/open-questions.md` | 持续更新 |
| CONTEXT.md 更新 | 项目根目录 `CONTEXT.md` | 实时更新 |
| ADR | `docs/adr/` | 按需创建 |

## Grill 状态

在 `collect-state.md` 中通过 `grill_mode` 字段跟踪：

- `grill_mode: on` — grill 进行中
- `grill_mode: off` — 未激活或已结束

`/prd-pause` 会同时暂停 grill；`/prd-resume` 恢复时 grill 状态不变（需要用户再次 `/prd-grill` 重新激活）。
`/prd-stop` 会结束 grill 并生成 battle 摘要。
