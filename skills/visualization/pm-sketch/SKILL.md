---
name: pm-sketch
description: 从 PMContext 生成全部草图（线框/信息架构/状态机/流程图）+ HTML 可交互原型。Use when generating sketches or prototype, or the user mentions 画草图、wireframe、prototype、可视化.
disable-model-invocation: true
---

# /pm-sketch

> 你是一位资深产品设计师，PMContext 已在手。你的任务是把 PMContext 中的页面定义、状态转移、流程步骤，变成**看得见的草图**——Mermaid 图让团队快速理解，HTML 原型让用户直接体验。

从 PMContext 生成全部可视化物。支持两种产出模式：
- **Mermaid 草图** — 线框、信息架构、状态机、流程图，写入 `sketch/*.md`
- **HTML 可交互原型**（`--prototype`）— 单页 HTML 高保真原型，可直接在浏览器打开

## Purpose

从 PMContext 生成全部可视化物：Mermaid 草图 + HTML 可交互原型。草图是 PMContext 的 View——每个图元必须可追溯到 PMContext 事实项。

## Context

PMContext 已沉淀页面定义、状态转移、流程步骤。本 skill 将这些转化为看得见的草图。

## Instructions

读取 `docs/pm-context/pm-context.md`。若不存在：
- 如果有 `$ARGUMENTS` → 自动调用 `/pm-need $ARGUMENTS` 全链路后回到草图生成
- 如果没有 → 🔴 STOP：提示先运行 `/pm-need`

- [ ] PMContext 已读取且非空
- [ ] 页面定义/状态转移/流程步骤/实体关系全部提取
- [ ] 调用 /pm-wireframe 生成线框图
- [ ] 调用 /pm-ia 生成信息架构图
- [ ] 调用 /pm-state 生成状态机图
- [ ] 调用 /pm-flow 生成流程图
- [ ] HTML 原型零外部依赖可离线预览
- [ ] [假设] 图元显式标注不伪装为确认设计
- [ ] 每个图元可追溯到 PMContext 事实项

## 启动模式

```
/pm-sketch                         → 正常模式：出全部四种 Mermaid 草图，停在审计门
/pm-sketch --prototype             → 高质量 HTML 可交互原型（含所有视图）
/pm-sketch --prototype --auto      → 自动模式：pm-need → PRD → 原型 零确认一气呵成
/pm-sketch --wireframe             → 只出线框图
/pm-sketch --ia                    → 只出信息架构图
/pm-sketch --state                 → 只出状态机图
/pm-sketch --flow                  → 只出流程图
/pm-sketch <需求描述>              → 自动模式：从需求描述开始全链路到草图
```

## 流程

### 1. 读取 PMContext

读取 `docs/pm-context/pm-context.md`，提取：
- 用户场景与目标
- 所有页面/功能定义（事实、规则、验收）
- 实体/关系定义
- 状态与状态转移
- 流程与步骤

若 PMContext 不存在且 `$ARGUMENTS` 不为空 → 自动调用 `/pm-need $ARGUMENTS` → 完成后继续。

### 2. 生成草图

#### 模式 A：Mermaid 草图（默认）

Run 四个子 Skill（按依赖顺序）：
1. `/pm-ia` → 信息架构：实体/页面关系
2. `/pm-state` → 状态机：状态转移
3. `/pm-flow` → 流程：步骤与分支
4. `/pm-wireframe` → 线框：页面布局

若 PMContext 中没有页面定义，信息架构图以实体关系为主体，跳过线框。

#### 模式 B：HTML 可交互原型（`--prototype`）

直接生成高质量 HTML 原型文件 `docs/pm-context/sketch/prototype.html`。

**HTML 原型模板结构**（Agent 按此模式生成，不要偏离此结构）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <!-- 使用内联 CSS，零外部依赖 -->
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语 */
  </style>
</head>
<body>
  <!-- 导航栏：标记当前页面位置 -->
  <nav>
    <a href="#page1">页面1</a>
    <a href="#page2">页面2</a>
  </nav>

  <!-- 每个页面一个 section，用 id 对应导航 -->
  <section id="page1">
    <h1>页面1: <名称></h1>
    <!-- 真实内容来自 PMContext 中的页面定义 -->
    <!-- 使用表格/卡片/列表等 HTML 原语表达数据结构 -->
  </section>

  <section id="page2">
    <h1>页面2: <名称></h1>
    <!-- ... -->
  </section>

  <script>
    // 交互：页面切换、表单验证、状态切换（可选）
    // 无外部 JS 依赖
  </script>
</body>
</html>
```

**质量清单**（生成后逐项检查）：
- ✅ 单页 HTML，零外部依赖（无 CDN 链接，Tailwind/React 均不可用）
- ✅ 响应式设计（移动端 ≤ 640px / 桌面端 ≥ 1024px 两套布局）
- ✅ 所有页面/组件都对应 PMContext 中的实体/关系
- ✅ 无法对应 PMContext 的图元标 `[假设]` 注释
- ✅ 交互可操作（点击/切换/表单输入等 demo 级别即可）
- ✅ UTF-8 编码，中文字符正常显示
- ✅ 文件容量 < 200KB（过大表示包含了不必要的复杂度）

**从 PMContext 到 HTML 图元的映射规则**：
| PMContext 中的项 | HTML 中的表达 |
|----------------|-------------|
| 页面/功能 | `<section id="<page-name>">` |
| 事实（字段/数据） | `<table>` 或 `<dl>` 列表 |
| 规则（业务逻辑） | `<p class="rule">` 带 🔴 标记 |
| 验收标准 | `<ul class="acceptance">` 清单 |
| 用户场景 | 页面顶部的场景描述文字 |
| 全局约束 | 页面底部的约束标注 |
| `[假设]` 项 | 标注 `--- [假设] 待确认 ---` 注释 |
| `[待确认]` 项 | 灰色占位 `<div class="placeholder">待确认: ...</div>` |

生成后自动输出：`✅ HTML 原型已生成: docs/pm-context/sketch/prototype.html`

### 3. 审计（仅非自动模式）

展示产出物清单：
- Mermaid 草图：4 个文件路径
- HTML 原型（如有）：文件路径
- PMContext 中未覆盖的图元（标 `[假设]`）

**🔴 CHECKPOINT** — 等用户确认。
- 用户说"通过" → 完成
- 用户说"调整" → 重新生成对应草图
- 用户说"继续" → 进入下个环节

## 零确认模式（--auto）

当通过 `--auto` 或直接 `$ARGUMENTS` 调用时：
1. 若 PMContext 不存在 → 自动 run `/pm-need --auto $ARGUMENTS`
2. 自动生成全部草图 + HTML 原型
3. 直接落盘完成，不等待确认
4. 输出产物清单 + 置信度摘要

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 且无 `$ARGUMENTS` | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 不存在但有 `$ARGUMENTS` 或 `--auto` | 自动调用 `/pm-need --auto $ARGUMENTS` 生成 PMContext，结束后回到草图生成 | pm-need 失败则 STOP 并提示失败原因 |
| PMContext 中无页面/实体定义 | 跳过 wireframe/ia，只生成 state/flow（若有规则线索）；顶部加 `⚠️ 跳过 N 个图：PMContext 缺页面/实体定义` | 不阻塞，记入信息缺口清单 |
| 任一子 skill（pm-wireframe/ia/state/flow）失败 | 不阻塞其他子 skill，记录失败项到产物清单的"失败清单"章节 | 其他成功草图仍落盘 |
| `--prototype` 模式下 HTML 文件 > 200KB | 拒绝落盘，提示"HTML 过大（N KB），精简后重试" | 退化为只输出 Mermaid 草图，不生成 HTML |
| `--prototype` 模式下 HTML 含外部 CDN 依赖 | 检测 `<link>`/`<script src="http">` 并移除，改为内联 | 无法内联则降级为纯 HTML 无样式 |
| `--auto` 模式下 pm-need 链路失败 | STOP 并输出一站式报告含失败原因 | 已生成部分仍落盘 |
| PMContext 中 `[冲突]` 项涉及核心图元 | 图元标 `[冲突]` 不强行选定方向 | 在产物清单汇总冲突项供 PM 决策 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 脱离 PMContext 凭感觉画图 | 图元无追溯，与需求脱节 |
| 把 `[假设]` 图元画成确定性内容 | 误导团队以为确认过 |
| HTML 依赖外部 CDN | 断网环境无法预览 |
| 草图嵌入 PRD 文件 | 草图是独立 View，不应嵌套 |
| `--auto` 遇子 skill 失败就全链路回滚 | 其他成功部分仍落盘，失败项单独标注 |

---

### Further Reading

- [Mermaid stateDiagram-v2 docs](https://mermaid.js.org/syntax/stateDiagram.html)
- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/examples-and-tips.md](references/examples-and-tips.md)。
