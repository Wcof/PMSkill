# PMSkill 评估集（Evals）

遵循 [Anthropic Agent Skills 官方建议](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration)的"先建评估再写文档"原则，为每个 skill 提供 ≥3 个评估场景与可判定的 rubric。

## 评估原则

- **数据驱动**：每个场景含 `skills`、`query`、`files`（可选）、`expected_behavior`（可判定行为清单）
- **覆盖关键失败模式**：每个 skill 的 eval 至少覆盖一个正常路径 + 一个边界/异常路径 + 一个反例
- **与 test-prompts.json 区分**：`test-prompts.json` 是开发期 smoke 测试（2 条/.skill，仅 happy path）；`evals/` 是正式评估集（≥3 条/skill，含 rubric），用于衡量 skill 在真实场景下的有效性

## 评估方法

### 准备

1. 在干净的 Agent 会话中加载待测 skill（及其依赖的下游 model-invoked skill）
2. 准备 `files` 字段声明的测试夹具文件（如示例 PMContext、mock 项目目录）
3. 按 `query` 发送指令，记录 Agent 完整行为轨迹

### 判定

对每个场景的 `expected_behavior` 列表逐条勾选：

- **PASS**：所有 expected_behavior 项全部满足
- **PARTIAL**：≥1 项未满足但核心目标达成
- **FAIL**：核心目标未达成或触发反例黑名单

### 模型覆盖

按官方建议在 Claude Haiku / Sonnet / Opus 三档模型上各跑一轮，记录：

- Haiku：指令是否足够明确（不足则补 SKILL.md）
- Sonnet：流程是否清晰高效
- Opus：是否避免过度解释

## 评估清单

| Skill | 评估文件 | 场景数 |
|---|---|---|
| pm-setup | [pm-setup.json](pm-setup.json) | 3 |
| pm-need | [pm-need.json](pm-need.json) | 4 |
| pm-collect | [pm-collect.json](pm-collect.json) | 3 |
| pm-refine | [pm-refine.json](pm-refine.json) | 3 |
| pm-prd | [pm-prd.json](pm-prd.json) | 3 |
| pm-aiprd | [pm-aiprd.json](pm-aiprd.json) | 3 |
| pm-humanprd | [pm-humanprd.json](pm-humanprd.json) | 3 |
| pm-premortem | [pm-premortem.json](pm-premortem.json) | 3 |
| pm-sketch | [pm-sketch.json](pm-sketch.json) | 3 |
| pm-wireframe | [pm-wireframe.json](pm-wireframe.json) | 3 |
| pm-ia | [pm-ia.json](pm-ia.json) | 3 |
| pm-state | [pm-state.json](pm-state.json) | 3 |
| pm-flow | [pm-flow.json](pm-flow.json) | 3 |

## 评估驱动开发循环

1. **Baseline**：先在不加载 skill 的情况下跑评估，记录失败/缺失上下文
2. **最小修复**：仅补充能通过评估的最小指令
3. **迭代**：跑评估 → 对照 baseline → 精炼 SKILL.md/references
4. **真实使用观察**：留意 Agent 实际访问文件的顺序、是否漏读 references、是否过度依赖某段——据此调整信息架构

## 夹具文件

部分评估需要预置的 PMContext 或 mock 项目结构，统一放在 `fixtures/` 下：

- `fixtures/pm-context.md` — 标准化的会员体系重构 PMContext 样本
- `fixtures/mock-project/` — 含 README/docs/TODO 标记的最小项目骨架
