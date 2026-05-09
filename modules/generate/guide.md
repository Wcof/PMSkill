# Generate 模块指南

## 职责

基于精炼与关联结果，生成可执行、可追溯的 PRD 文档与 **Agent Context**。在 PRD Context Compiler 中，Generate 产物是指导人或 Agent 实施的工程上下文，不只是文档摘要。

生成模块只负责把已经精炼、已经关联的上下文组织成可交付文档。生成阶段的文件是 **View**，不是新的 **Entity** 或事实来源。它不能替代精炼，也不能在缺少来源或关系时补写“看起来合理”的规则。

## 核心约束

1. **必须基于 refined 和 relations 生成，不允许凭空新增业务规则。**
2. 必须保留待确认问题。
3. 每个页面必须有目标、区域、字段、操作、状态。
4. 每个规则必须有条件、步骤、异常、权限。
5. 每个数据对象必须有字段语义和关系。
6. 每个核心功能必须有验收标准。
7. 必须生成 Agent 可执行上下文。
8. **AI 推断已标记。**
9. **生成文档不能脱离来源。**
10. **不得新增未来源化、未关联的业务规则。**
11. Check 是 **Soft Gate**：不默认阻断 `/prd-generate`，但未通过内容必须降级为风险或待确认。
12. 当前置产物缺失或 Check 未通过时，只能输出 **Limited Generate**，不能伪装成完整确定性 PRD。
13. 确定性要求必须来自 **Strong Trace**；**Weak Trace** 只能进入风险或待确认区。

## 输入

- `docs/prd-helper/02-refine/`
- `docs/prd-helper/03-relate/`

## 输出

输出到 `docs/prd-helper/04-generate/`：

```
04-generate/
├── overview/
│   └── project-overview.md          ← 模板: 04-generate-overview-template.md
├── pages/
│   └── {page-name}.md               ← 模板: 04-generate-page-prd-template.md
├── rules/
│   └── {rule-name}.md               ← 模板: 04-generate-rule-prd-template.md
├── data/
│   └── {data-name}.md               ← 模板: 04-generate-data-prd-template.md
├── acceptance/
│   └── {feature-name}.md            ← 模板: 04-generate-acceptance-template.md
├── agent-context/
│   ├── frontend-context.md           ← 模板: 04-generate-agent-context-template.md
│   ├── backend-context.md
│   ├── test-context.md
│   └── product-review-context.md
└── check.md                          ← 模板: 04-generate-check-template.md
```

## 验收条件

- 不凭空新增业务规则
- 保留待确认问题
- 页面/规则/数据/验收结构完整
- 生成前后可追溯（每份文档包含来源说明）
- 角色覆盖完整（产品经理、前端、后端、测试、产品复核、Agent）
- 输出 `check.md`

## Agent 上下文边界

`agent-context/` 是给后续执行者使用的上下文，不是新的 PRD 来源。它必须来自 `02-refine/` 和 `03-relate/`：

| 文件 | 服务对象 | 必须包含 |
|------|----------|----------|
| `frontend-context.md` | 前端与 UI Agent | 页面、字段、操作、状态、前端验收和禁推断项 |
| `backend-context.md` | 后端与接口 Agent | 规则、数据、状态变化、异常、权限和来源 |
| `test-context.md` | 测试与 QA Agent | 验收范围、边界、异常、回归影响和待确认问题 |
| `product-review-context.md` | 产品复核 | 背景、目标、决策、冲突、问题、推断和来源说明 |

如果某项内容没有来源或没有关联链路，应保留为待确认或风险项，不得在 Agent Context 中写成确定要求，不能写成确定性要求。

Agent Context 必须继承 View 边界：它可以组织事实、关系、验收、风险和禁止实施项，但不能成为新的事实来源，也不能把 Weak Trace 或断链内容写成确定性要求。

## Limited Generate

`/prd-generate` 永远可以执行。若 `02-refine/`、`03-relate/`、Strong Trace 或关系链路不足，输出属于 **Limited Generate**：

- 缺失来源、Weak Trace、断链、待确认问题必须显式列出。
- 禁止实施项必须进入 PRD 和 Agent Context 的风险区。
- 受限生成结果仍是 View，不是 Entity，也不是完整确定性 PRD。

## Generate Manifest

Generate Manifest 是生成阶段的全量 View 清单。它从 `02-refine/` 和 `03-relate/` 推导出一次 `/prd-generate` 应该产出的所有 View，包括：

- `overview/project-overview.md`
- `pages/{page_id}.md`
- `rules/{rule_id}.md`
- `data/{data_id}.md`
- `acceptance/{acceptance_id}.md`
- `agent-context/frontend-context.md`
- `agent-context/backend-context.md`
- `agent-context/test-context.md`
- `agent-context/product-review-context.md`
- `check.md`

判断“是否一次性生成完所有 PRD”必须以 Generate Manifest 为准，而不是只检查已经存在的文件。

## Generate Runner

`/prd-generate` 通过 Generate Runner 执行 `manifest -> scaffold/generate -> check`：

1. 构建 Generate Manifest。
2. 创建缺失的 View 路径。
3. 保留已有用户内容，不默认覆盖。
4. 写出 `04-generate/check.md`。
5. 输出 created/existing/skipped/limited/failed 摘要。

## Quality Report

`04-generate/check.md` 是结构化 Quality Report 的 View。质量判断至少包含：

- Manifest 覆盖率：应有 View、已有 View、缺失 View、非预期 View。
- 模板完整性：各 View 是否满足对应章节结构。
- Traceability：生成内容是否保留来源或关系锚点。
- Relation Chain：断链内容是否进入风险或待确认区。
- Agent Context Safety：Weak Trace、断链和缺失来源是否被禁止写成确定性要求。
- Limited Generate：前置缺失和禁止实施项是否显式暴露。

## 逐文件验收条件

| 文件/目录 | 验收条件 |
|-----------|----------|
| `overview/project-overview.md` | 项目背景、业务目标、角色、范围、模块、流程、约束、非目标、待确认问题和来源说明完整 |
| `pages/*.md` | 每个页面有基本信息、区域、字段、操作、状态、异常、权限、前端验收、待确认问题和来源说明 |
| `rules/*.md` | 每条规则有目标、触发页面/操作、前置条件、步骤、状态变化、异常、权限、审计、数据、接口用途、验收和来源说明 |
| `data/*.md` | 每个数据域有对象、关系、字段、状态、生命周期、来源、去向、表结构关系、待确认问题和来源说明 |
| `acceptance/*.md` | 验收范围、页面/功能/规则/数据/异常/权限/边界/回归影响和来源说明完整 |
| `agent-context/*.md` | 前端、后端、测试、产品复核上下文均包含任务背景、事实、禁推断项、页面、规则、数据、验收和输出要求 |
| `check.md` | 使用 `04-generate-check-template.md`，并能引用 `check-generated.py` 的检查结果 |

## 检查

使用 `templates/04-generate-check-template.md` 生成 `check.md`。

检查要点：
- 来源检查（内容来自 refine/relate，无凭空规则，推断已标记，问题已保留）
- 结构检查（各类型文档结构完整）
- 角色覆盖检查（各角色可读/可执行/可验收）
- Limited Generate 风险检查（前置缺失、Weak Trace、断链和禁止实施项显式保留）

## 自动化校验

可运行脚本验证生成质量：

```bash
python3 modules/generate/scripts/check-generated.py docs/prd-helper
```

脚本从模板自动读取必填章节，确保模板和校验同步。

## 下一步

通过检查后进入 **Final Check（最终总检查）** 阶段。
