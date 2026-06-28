---
name: pm-collect
description: 主动深度扫描 URL、项目、知识库和对话上下文，收集材料并按类型聚合。Use when materials are needed before refining, or the user mentions feedback, meeting notes, raw context.
---

# /pm-collect

> 你是一位资深产品经理，正在进行一次产品需求调研。你的任务是尽可能多地从各个来源搜集原始材料——不筛选、不推断、不取舍。**能扫到的绝不问，能推断的绝不等**。

主动收集材料，无需 PM 手动喂入。从四个来源自动深度扫描，整理后落盘。核心设计原则：**能扫到的绝不问，能推断的绝不等**。

## Purpose

主动收集材料，无需 PM 手动喂入。从四个来源自动深度扫描，整理后落盘。collect 只整理不改写——事实提取留给 refine。

## Context

PM 提供了需求描述和可能的 URL，项目中有散落信息。本 skill 主动扫描所有来源，按类型聚合，建立材料间关联。

## Instructions

`/pm-need` 传入的 `$ARGUMENTS` 作为收集种子：
- 提取需求描述（一句话需求）作为核心主题
- 提取其中所有 URL，逐个抓取

- [ ] 需求描述（一句话核心主题）已提取
- [ ] 所有 URL 逐个抓取（失败的显式标注不静默跳过）
- [ ] 对话上下文材料已提取
- [ ] 项目深扫描完成（目录结构/git commits/TODO-FIXME/配置文件）
- [ ] 知识库按需搜索（若已配置）
- [ ] 4 源材料按类型聚合为单 md 并去重
- [ ] 材料间关联关系已建立
- [ ] 整理后材料落盘到 `docs/pm-context/collect/`

## 来源（按优先级）

### 1. URL 抓取
从 `$ARGUMENTS` 中提取所有 URL，逐个抓取并解析：
- 网页 URL（http/https）— 抓取页面内容，提取正文（忽略导航/广告/脚注等噪音）
- 文档链接（Notion、飞书文档、Google Docs 等公开分享链接）— 抓取可访问内容
- 抓取失败时标 `[待确认]`，记录原始 URL，不阻塞后续流程——但记录到信息缺口
- 来源标注为 `URL: <原始链接>`

### 2. 对话上下文
PM 在当前对话中说/粘贴的内容——直接提取，无需额外操作。

### 3. 项目深扫描
主动深度扫描当前项目，提取与产品需求相关的信息。扫描范围：

按以下命令逐个执行，扫描结果写入 `docs/pm-context/collect/` 下的对应章节。

#### 3.1 根级文件
```bash
# 扫描根级配置文件——了解技术栈、项目描述、Agent 配置
for f in README.md CONTEXT.md CLAUDE.md AGENTS.md .atomcode.md CHANGELOG.md SECURITY.md SKILL.md; do
  if [ -f "$f" ]; then
    echo "=== $f (wc -c) $(wc -c < "$f")==="
    head -50 "$f"
  fi
done
# 扫描包管理器配置——确定技术栈
for f in package.json pyproject.toml Cargo.toml go.mod composer.json Gemfile; do
  if [ -f "$f" ]; then head -30 "$f"; fi
done
```
扫描要点：README.md（项目概述、技术栈）、CONTEXT.md（领域术语）、CLAUDE.md/AGENTS.md（Agent 配置——已有 PMSkill 配置说明该 Skill 已被使用）、CHANGELOG.md（版本变更历史）、package.json/pyproject.toml 等（技术栈与依赖）。

#### 3.2 docs/ 目录全量扫描
```bash
# 递归扫描 docs/ 下所有 md 文件——提取文件名、一级标题、摘要
for f in $(find docs/ -name "*.md" -type f 2>/dev/null); do
  echo "=== $f ==="
  head -1 "$f"
  echo "--- 摘要(前200字) ---"
  head -20 "$f" | fold -w 200 | head -1
  echo ""
done
```
重点提取：需求文档、设计文档、ADR、用户手册、API 文档。每个文件提取文件名、一级标题、前 200 字摘要。

#### 3.3 git 仓库元数据（若为 git 仓库）
```bash
# 最近 30 条 commit——了解项目演进脉络
git log --oneline -30 2>/dev/null || echo "非 git 仓库，跳过"
# 当前分支与主分支差异
git diff --stat main...HEAD 2>/dev/null || echo "无法对比分支"
```
从 commit message 提取：正在做的功能方向、已修复的 bug、重构计划。

#### 3.4 源码中的标记（轻量扫描）
```bash
# 扫描 TODO/FIXME/HACK——发现已知问题和未完成功能
grep -rn "TODO\|FIXME\|HACK" src/ app/ lib/ components/ pages/ services/ \
  --include="*.ts" --include="*.tsx" --include="*.py" --include="*.rs" \
  --include="*.go" --include="*.java" --include="*.js" 2>/dev/null | head -30
```
只收集业务逻辑相关的标记（"TODO: 添加支付"、"FIXME: 用户登录超时"等），忽略纯技术性标记（"TODO: 重构这个函数"等）。用于发现项目中的"已知问题"和"未完成功能"。

#### 3.5 目录结构与命名模式
```bash
# 获取主源码目录结构——理解模块划分和命名约定
for d in src app lib components pages services api routes models; do
  if [ -d "$d" ]; then
    echo "--- $d/ ---"
    ls -R "$d" 2>/dev/null | head -40
  fi
done
```
通过目录名和文件名推断：是否按功能模块组织？是否有特定命名约定？模块间依赖关系如何？

### 4. 知识库搜索
若 `/pm-setup` 配置了知识库路径，搜索知识库中与当前需求相关的文档：
- 读取知识库目录下的所有 `*.md` 文件索引（文件名 + 一级标题 + 摘要）
- 根据当前对话主题，筛选与需求相关的文档
- 提取相关段落（整篇文档太大时只提取相关章节）
- 知识库材料来源标注为 `知识库: <文件路径>`

知识库典型内容：竞品分析报告、用户调研结果、行业报告、历史 PRD、业务规则文档、合规要求等。

## 产物

收集后整理到 `docs/pm-context/collect/` 目录，按材料类型聚合为一个 md 文件（避免文件过多增加大模型理解成本）：

```markdown
# <类型名>（如：会议纪要、项目扫描发现、网页抓取）
## <具体材料1标题>
### 来源索引
- 来源：URL / 对话 / 项目深扫描 / 知识库
- 路径：<原始 URL 或文件路径>
- 时间：<收集时间>
### 概要
<一段话总结>
### 关键信息
- <关键点1>
- <关键点2>
### 与其他材料的关联
- 与 <材料X> 互相印证/矛盾
## <具体材料2标题>
...
```

项目深扫描发现特别标注 `来源: 项目深扫描`，并注明扫描了哪些区域。

## 关联增强

整理时建立材料之间的关联（如：同一主题的多条反馈、互相印证或矛盾的材料）。

## 完成信号

正常模式：`/pm-collect` 完成后，输出："收集了 N 条材料（来源：URL U 条 / 对话 M 条 / 项目深扫描 K 条（docs/N 个、git/M 条、标记/L 处、配置/O 个） / 知识库 L 条），概要如下"。**无需 PM 确认**，直接进入 `/pm-refine`。

**🟡 WARNING**：如果所有 URL 都抓取失败（死链），且项目扫描和对话上下文材料过少（< 3 条），触发警告：材料过少，refine 推断将高度依赖 URL 材料以外的有限上下文。标记到信息缺口清单。

**🔴 CHECKPOINT**：collect 完成后若材料总量 < 5 条，提示 PM"当前材料较少（仅 N 条），需补充 URL 引用或粘贴更多上下文后再进入 refine 阶段"。PM 可决定继续或补充。

## 产出示例 · 延伸参考 · 实战提示

详见 [references/examples-and-tips.md](references/examples-and-tips.md)。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/collect/` 目录不存在 | 自动创建 | 不阻塞 |
| URL 抓取失败（死链/超时/403） | 重试 1 次，仍失败则记入"抓取失败清单" | 不阻塞，标到信息缺口 |
| 项目深扫描某子项失败（如非 git 仓库） | 跳过该子项，标注"非 git 仓库，跳过 git 元数据" | 不阻塞，继续其他子项 |
| 知识库路径无效（pm-setup 配置的路径不存在） | 提示"知识库路径无效，跳过知识库扫描" | 不阻塞，标到信息缺口 |
| 材料总量 < 5 条 | 🟡 WARNING + 🔴 CHECKPOINT 提示 PM 是否继续 | PM 选继续则进入 refine；选补充则等 PM 加材料 |
| 所有 URL 死链且项目扫描 + 对话材料 < 3 条 | 🟡 WARNING 标记到信息缺口清单 | 不阻塞，但 refine 推断将高度依赖有限上下文 |
| 4 源材料去重时发现完全重复 | 保留首条，后续标 `← 重复: <首条材料 id>` | 不阻塞 |
| TODO/FIXME 标记全是纯技术性（无产品含义） | 不收集，标注"扫描到 N 处 TODO/FIXME 但无产品含义" | 不阻塞 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 在 collect 阶段提取事实或改写原文 | collect 只整理材料，事实提取是 refine 的职责 |
| 原样堆文件不整理、文件之间无关联 | refine 需要看关联关系才能推断冲突和一致性 |
| 一个材料一个文件导致文件过多 | 按类型聚合为单 md，减少大模型理解成本 |
| 项目扫描只扫 README 不扫 docs/ | docs/ 中往往有设计决策和需求文档 |
| 忽略 git commit history | commit message 中蕴含了产品决策和演进 |
| 扫描到 TODO/FIXME 但不标注其产品含义 | PM 需要知道这些标记对应的功能方向 |
| 4 �源材料不去重导致 refine 重复推断 | 去重是 collect 的职责，重复材料增加 refine 成本 |

---

### Further Reading

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
