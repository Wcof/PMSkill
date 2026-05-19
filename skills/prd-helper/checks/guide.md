# Checks 指南

`checks/` 是横向 **Soft Gate（软门禁）**，不是第五业务模块。Soft Gate 服务于 PRD Context Compiler：它默认不硬阻断用户命令，但必须暴露来源缺失、断链、结构缺口和待确认风险。

当 Soft Gate 未通过时，后续命令仍可执行；但未通过内容只能进入风险或待确认区，不能写成确定性 PRD 或 **Agent Context** 要求。当前置产物缺失或检查未通过时，Generate 输出属于 **Limited Generate**。

生成阶段文档是 **View**，不是 **Entity**。只有跨阶段流转、需要被引用、需要 ID、需要参与关系链路的对象才是实体。检查也必须区分 **Strong Trace** 与 **Weak Trace**：具备 `source_id + path + quote/paraphrase + locator` 的内容才可进入确定性要求，Weak Trace 只能进入风险或待确认区。

## 检查架构

检查系统由三层组成，共享同一套规则：

```
模块指南（行为约束）
    ↓
检查模板（人类可读检查清单）    ←  modules/*/templates/*-check-template.md
    ↓
自动化脚本（机器可执行校验）    ←  modules/*/scripts/check-*.py
```

### 单一来源原则

- **行为约束**定义在各模块指南（`modules/*/guide.md`）的"核心约束"和"检查"章节
- **检查模板**在 `modules/*/templates/*-check-template.md`，由 agent 填写
- **自动化脚本**在 `modules/*/scripts/`，从模板和 ID 注册表动态读取校验规则

### ID 注册表

所有实体类型（fact、rule、page 等）的前缀、必填字段、文件名统一定义在 `scripts/lib/id_registry.py`。

新增实体类型时只需修改注册表，脚本自动适配。

## 覆盖范围

| 阶段 | 检查模板 | 自动化脚本 | 检查产物 |
|------|----------|-----------|---------|
| 采集后 | `01-collect-check-template.md` | `check-collect.py`（状态+结构） | `01-collect/check.md` |
| 精炼后 | `02-refine-check-template.md` | `check-refine.py`（分类+来源+风险） | `02-refine/check.md` |
| 关联后 | `03-relate-check-template.md` | `check-relate.py`（断链+孤立项+待确认影响） | `03-relate/check.md` |
| 生成后 | `04-generate-check-template.md` | `check-generated.py`（结构+内容+来源+待确认汇总） | `04-generate/check.md` |
| 最终 | `05-final-check-template.md` | `check-structure.py`（目录完整性） | `05-check/*.md` |

## 检查产物位置

检查产物统一输出到目标项目 `docs/prd-helper/` 各阶段目录与 `05-check/`。

- `01-collect/check.md`
- `02-refine/check.md`
- `03-relate/check.md`
- `04-generate/check.md`
- `05-check/full-check.md`
- `05-check/gap-check.md`
- `05-check/relation-check.md`
- `05-check/source-check.md`
- `05-check/generated-check.md`
- `05-check/context-delta.md`
- `05-check/structure-check-result.md`

## 模板

- `checks/templates/05-final-check-template.md` — 最终总检查清单
- `checks/templates/05-context-delta-template.md` — 本轮上下文增量

## 自动化脚本

```bash
# 检查采集模块状态和结构
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect

# 检查精炼分类、来源与风险
python3 modules/refine/scripts/check-refine.py docs/prd-helper

# 检查关联断链、孤立项与待确认影响范围
python3 modules/relate/scripts/check-relate.py docs/prd-helper

# 检查目录结构完整性
python3 scripts/check-structure.py docs/prd-helper

# 检查生成文档完整性和质量
python3 modules/generate/scripts/check-generated.py docs/prd-helper
```

脚本使用 `scripts/lib/id_registry.py` 中的实体定义，与模板保持同步。
