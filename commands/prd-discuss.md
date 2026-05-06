---
description: 开启需求研讨模式 — 追问矛盾、模糊术语和未决问题
allowed-tools: Bash, Read
---

# /prd-discuss

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

## Step 0: 定位 Skill 并检查前置条件

```bash
set -euo pipefail

find_prd_helper_root() {
  for dir in ".claude/skills/prd-helper" ".agents/skills/prd-helper" "."; do
    [ -f "$dir/modules/grill/guide.md" ] && { printf '%s\n' "$dir"; return 0; }
  done
  return 1
}

skill_root="$(find_prd_helper_root)" || {
  echo "未找到 PRD Helper 安装目录。请先运行：npx skills@latest add Wcof/PRDContextEngine --agent claude-code --skill prd-helper -y"
  exit 1
}

echo "Skill root: $skill_root"
```

读取 `collect-state.md`，检查 `capture_mode` 是否为 `on`。如果不是，提示用户先执行 `/prd-start`。

读取 `$skill_root/modules/grill/guide.md` 了解完整行为规则。

## Step 1: 确保研讨目录存在

```bash
mkdir -p docs/prd-helper/01-collect/grill
```

## Step 2: 扫描已采集材料

读取以下目录的所有文件：
- `docs/prd-helper/01-collect/active/`
- `docs/prd-helper/01-collect/passive/`

梳理发现的：
- 矛盾点（同一概念在不同来源中说法不同）
- 模糊术语（定义不清、用法不一致）
- 未解决的冲突（需求之间互相矛盾）
- 遗漏项（明显缺失的关键信息）

## Step 3: 呈现发现并询问方向

向用户汇报扫描结果，然后询问：

> "我发现了以下矛盾/模糊点：
> 1. ...
> 2. ...
>
> 你想先讨论哪一个？如果你有新的命题，也可以直接给我。"

等待用户选择。

## Step 4: 进入持续研讨模式

更新 `collect-state.md`，设置 `grill_mode: on`。

然后进入持续质询循环，遵循以下规则（来自 `modules/grill/guide.md`）：

### 核心行为

- 逐个问题追问，等用户回答后再继续
- 每个问题附带你的推荐答案
- 如果问题可以通过读代码/文档回答，先探索再提问
- 每个回答都要说明应该沉淀到 facts、decisions、conflicts、questions、assumptions 或 CONTEXT.md 中的哪一类

### 挑战术语表

当用户使用的术语与项目 `CONTEXT.md` 冲突时，立即指出。

### 模糊语言精炼

当用户使用模糊或重载的术语时，提出精确的规范术语。

### 具体场景压力测试

构造探测边界情况的场景，迫使用户精确说明概念之间的边界。

### 交叉引用

当用户陈述某件事如何工作时，检查代码/文档是否一致。发现矛盾时指出。

### 实时更新 CONTEXT.md

术语澄清后，立即更新项目根目录的 `CONTEXT.md`。格式见 `modules/grill/templates/CONTEXT-FORMAT.md`。

### 谨慎提供 ADR

同时满足"难以逆转 + 没有上下文令人惊讶 + 真实权衡结果"时才提议创建 ADR。格式见 `modules/grill/templates/ADR-FORMAT.md`。

## Step 5: 结束需求研讨

当用户表示研讨结束（或触发 `/prd-stop`）时：

1. 更新 `collect-state.md`，设置 `grill_mode: off`
2. 生成 `docs/prd-helper/01-collect/grill/discussion-summary.md`，包含：
   - 已解决的问题列表
   - 未解决的开放问题
   - 术语变更记录
   - 创建的 ADR 列表
3. 更新 `docs/prd-helper/01-collect/grill/open-questions.md`（仅未解决问题）
