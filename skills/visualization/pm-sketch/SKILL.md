---
name: pm-sketch
description: 从 PMContext 生成全部草图（线框/信息架构/状态机/流程图）+ HTML 可交互原型（--prototype）。支持 --auto 零确认模式与单图模式（--wireframe/--ia/--state/--flow）。Use when generating sketches or prototypes from PMContext, or the user mentions 草图、sketch、线框、原型、可视化、prototype、交互原型、Mermaid.
disable-model-invocation: true
---

# /pm-sketch

> 你是一位资深产品设计师，PMContext 已在手。你的任务是把 PMContext 中的页面定义、状态转移、流程步骤，变成**看得见的草图**——Mermaid 图让团队快速理解，HTML 原型让用户直接体验。

从 PMContext 生成全部可视化物。支持两种产出模式：
- **Mermaid 草图** — 线框、信息架构、状态机、流程图，写入 `sketch/*.md`
- **HTML 可交互原型**（`--prototype`）— 技术栈自适应的可交互原型，可直接在浏览器打开

## Purpose

从 PMContext 生成全部可视化物：Mermaid 草图 + HTML 可交互原型（技术栈自适应）。草图是 PMContext 的 View——每个图元必须可追溯到 PMContext 事实项。

## Context

PMContext 已沉淀页面定义、状态转移、流程步骤。本 skill 将这些转化为看得见的草图。**技术栈感知**：生成 HTML 原型前先确定技术栈——已有代码的项目自动检测，新项目推荐当前流行技术栈。

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
- [ ] HTML 原型前已完成技术栈决策（新项目推荐 / 老项目检测）
- [ ] HTML 原型使用推荐/检测到的技术栈 CDN 生成
- [ ] [假设] 图元显式标注不伪装为确认设计
- [ ] 每个图元可追溯到 PMContext 事实项

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的草图编排职责：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（草图） | 编排 4 个子 Skill 生成全部草图，确保每个图元追溯到 PMContext 实体/关系 | 不回灌（产出 View） |

执行时依次调用 /pm-ia → /pm-state → /pm-flow → /pm-wireframe。子 Skill 各自写入 `.loop/` 中间工件。

**产出约束**：
- 每个图元必须对应 PMContext 中的实体/关系，无法对应的标 `[假设]`
- 步骤 5 的 Launch-Blocking Tiger 涉及的实体必须在草图中有对应图元
- 必须产出**草图交付物清单**：4 个 Mermaid 文件路径 + [假设] 图元数 + 未覆盖 Tiger 实体数
- HTML 原型（--prototype）：使用推荐/检测到的技术栈 CDN 生成、< 200KB（不含 CDN 外部资源）、响应式

**依赖检查**：是否有未追溯到 PMContext 的图元？步骤 5 的 Tiger 实体是否在草图中覆盖？HTML 原型是否通过质量清单？

## 启动模式

```
/pm-sketch                         → 正常模式：出全部四种 Mermaid 草图，停在审计门
/pm-sketch --prototype             → 高质量 HTML 可交互原型（含所有视图）
/pm-sketch --prototype --auto      → 自动模式：pm-need → premortem → PRD → 原型 零确认一气呵成
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

生成技术栈自适应的 HTML 原型文件 `docs/pm-context/sketch/prototype.html`。

**Step 0：技术栈决策**

生成原型前，先确定技术栈：

1. **扫描项目已有代码**：检查根目录及常见子目录
   - 检测 `package.json` → 读取 `dependencies`/`devDependencies` 中的框架
   - 检测 `vue.config.js` / `nuxt.config.ts` / `vite.config.ts` → Vue3 生态
   - 检测 `next.config.js` / `tsconfig.json` → React / TypeScript
   - 检测 `electron-builder.json` / `electron/` 目录 → Electron
   - 检测 `flutter/` / `pubspec.yaml` → Flutter（HTML 原型不适用，标注）
   - 检测 `Cargo.toml` 含 `tauri` → Tauri（HTML 原型不适用，标注）
   - 检测 `angular.json` → Angular
2. **判断**：
   - 检测到已有技术栈 → 使用该技术栈的 CDN 版本生成原型
   - 未检测到代码（新项目）→ 按 PMContext 中的产品类型推荐技术栈
3. **输出技术栈决策**：`✅ 技术栈: <名称>（<依据: 检测到依赖 / 新项目推荐>）`

**新项目技术栈推荐规则**：

| 产品类型（从 PMContext 推断） | 推荐技术栈 |
|---------------------------|-----------|
| 业务管理系统 / 后台管理 | Vue3 + Vite + TypeScript + Element Plus |
| 前端页面 / 官网 / 营销页 | Vue3 + Vite + TailwindCSS + TypeScript |
| 桌面客户端应用 | Electron + Vue3 + Vite + TypeScript |
| 移动端 App | Flutter / React Native（HTML 原型不适用，输出设计说明） |
| 全栈 Web 应用 | Vue3 + Nuxt + TypeScript / React + Next.js + TypeScript |
| 微前端架构 | Vue3 + Vite + Module Federation + TypeScript |
| 默认（无法推断产品类型） | Vue3 + Vite + TypeScript（最通用） |

**HTML 原型模板**（完整代码见 [references/prototype-templates.md](references/prototype-templates.md)，按技术栈选择对应模板，不要偏离核心结构）：
- Vue3 CDN → 检测到 Vue3 或推荐 Vue3 时使用
- React CDN → 检测到 React 或推荐 React 时使用
- Plain HTML 兜底 → 检测到 Angular / 无框架 / 冲突 / CDN 不可达时使用

**Electron 适配**：生成 Vue3/React 版本，在原型顶部加 `<!-- 🖥 此原型推荐用 Electron 包装运行 -->`

**移动端适配**：Flutter/React Native → 输出 `design-spec.md` 替代 HTML 原型

**质量清单**（生成后逐项检查，完整清单见 [references/prototype-templates.md](references/prototype-templates.md)）：
- ✅ 技术栈决策有依据
- ✅ 使用推荐/检测到的技术栈 CDN 版本
- ✅ 响应式设计（移动端 ≤ 640px / 桌面端 ≥ 1024px）
- ✅ 所有图元对应 PMContext 实体/关系
- ✅ 原型文件 < 200KB（不含 CDN 外部资源）

**从 PMContext 到 HTML 图元的映射规则**：
| PMContext 中的项 | HTML 中的表达 |
|----------------|-------------|
| 页面/功能 | `<section id="<page-name>">` 或 Vue `v-for` / React `map` |
| 事实（字段/数据） | `<table>` 或 `<dl>` 列表，或 Vue `v-for` / React `map` |
| 规则（业务逻辑） | `<p class="rule">` 带 🔴 标记 |
| 验收标准 | `<ul class="acceptance">` 清单 |
| 用户场景 | 页面顶部的场景描述文字 |
| 全局约束 | 页面底部的约束标注 |
| `[假设]` 项 | 标注 `--- [假设] 待确认 ---` 注释 |
| `[待确认]` 项 | 灰色占位 `<div class="placeholder">待确认: ...</div>` |

生成后自动输出：
- `✅ 技术栈: <名称>（<依据>）`
- `✅ HTML 原型已生成: docs/pm-context/sketch/prototype.html`

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
| `--prototype` 模式下无法检测到技术栈（无代码、无 package.json、无依赖） | 按新项目推荐 Vue3 + Vite + TypeScript | 使用 Plain HTML 兜底模板 |
| `--prototype` 模式下检测到多个冲突框架（如 package.json 同时含 vue 和 react） | 标 `[冲突]` 并列出检测到的框架，推荐使用第一个 | 使用 Plain HTML 兜底模板，避免偏向某一方 |
| `--prototype` 模式下推荐/检测到 Flutter / React Native（HTML 原型不适用） | 输出 `design-spec.md` 替代 HTML 原型，包含屏幕设计说明 + 组件规范 + 交互描述 | 不生成 prototype.html，在产物清单中标注 |
| `--prototype` 模式下 HTML 文件生成体量 > 200KB | 拒绝落盘，提示"原型内容过多（N KB），精简后重试" | 退化为只输出 Mermaid 草图，不生成 HTML |
| `--prototype` 模式下 CDN 版本不可用（如 unpkg CDN 域名被墙） | 使用备用 CDN（cdnjs / jsdelivr），或退化为 Plain HTML 兜底模板 | 退化为 Plain HTML 无框架版本 |
| `--auto` 模式下 pm-need 链路失败 | STOP 并输出一站式报告含失败原因 | 已生成部分仍落盘 |
| PMContext 中 `[冲突]` 项涉及核心图元 | 图元标 `[冲突]` 不强行选定方向 | 在产物清单汇总冲突项供 PM 决策 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 脱离 PMContext 凭感觉画图 | 图元无追溯，与需求脱节 |
| 把 `[假设]` 图元画成确定性内容 | 误导团队以为确认过 |
| 原型使用与推荐/检测技术栈无关的 CDN | 原型的目的是展示开发方向，用错技术栈给 PM 和工程团队错误预期 |
| 有现有代码时不检测技术栈，直接用默认模板 | 老项目已有可用的框架/组件库，用新技术栈生成的原型与实际开发脱节 |
| 新项目不推荐技术栈 | PM 需要技术方向建议来评估可行性和资源 |
| 草图嵌入 PRD 文件 | 草图是独立 View，不应嵌套 |
| `--auto` 遇子 skill 失败就全链路回滚 | 其他成功部分仍落盘，失败项单独标注 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"经过分析得到" | 空话，必须写明是同义词推导/多对多实体映射/边界隔离分析之一（ADR 0008 §11） |

---

### Further Reading

- [Mermaid stateDiagram-v2 docs](https://mermaid.js.org/syntax/stateDiagram.html)
- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/sketch-prototype-example.md](references/sketch-prototype-example.md)（草图 + HTML 原型联动产出示例与 9 项质量检查技巧）。
