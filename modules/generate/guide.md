# Generate 模块指南

## 职责

基于精炼与关联结果，生成可执行、可追溯的 PRD 文档与 Agent 上下文。

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
- 角色覆盖完整（产品经理、前端、后端、测试、Agent）
- 输出 `check.md`

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

## 自动化校验

可运行脚本验证生成质量：

```bash
python3 modules/generate/scripts/check-generated.py docs/prd-helper
```

脚本从模板自动读取必填章节，确保模板和校验同步。

## 下一步

通过检查后进入 **Final Check（最终总检查）** 阶段。
