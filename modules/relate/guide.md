# Relate 模块指南

## 职责

建立需求、页面、功能、规则、数据、验收之间的关系链路，确保不再断链。

## 核心约束

1. 每个需求事实必须关联到页面或功能。
2. 每个功能必须关联到业务规则。
3. 每个业务规则必须关联到数据对象。
4. 每个业务规则必须关联到验收标准。
5. 待确认问题必须关联影响范围。
6. **不允许存在孤立需求、孤立页面、孤立规则、孤立数据、孤立验收。**

## 关联关系

```
需求事实 → 页面
需求事实 → 功能
功能 → 业务规则
业务规则 → 数据对象
页面 → 字段
页面 → 操作
页面 → 接口用途
业务规则 → 验收标准
业务规则 → 异常场景
待确认问题 → 影响范围
```

## 输入

- `docs/prd-helper/02-refine/` 下的精炼结果

## 输出

输出到 `docs/prd-helper/03-relate/`：

| 文件 | 用途 | 模板 |
|------|------|------|
| `page-map.md` | 页面关联 | `03-relate-page-map-template.md` |
| `feature-map.md` | 功能关联 | `03-relate-feature-map-template.md` |
| `rule-map.md` | 规则关联 | `03-relate-rule-map-template.md` |
| `data-map.md` | 数据关联 | `03-relate-data-map-template.md` |
| `acceptance-map.md` | 验收关联 | `03-relate-acceptance-map-template.md` |
| `context-map.md` | 上下文总关联 | `03-relate-context-map-template.md` |
| `check.md` | 关联检查 | `03-relate-check-template.md` |

## ID 命名约定

每条实体使用 `{前缀}_NNN` 格式（如 `page_001`、`rule_002`）。

完整实体类型定义见 `scripts/lib/id_registry.py`。

## 验收条件

链路规则的脚本权威来源是 `scripts/lib/id_registry.py` 中的 `RELATION_CHAIN_RULES`。

- 每个 fact 关联到页面或功能
- 每个 feature 关联到规则
- 每个 rule 关联到数据对象
- 每个 rule 关联验收标准
- 待确认问题关联影响范围
- 无孤立需求、孤立页面、孤立规则、孤立数据、孤立验收
- 输出 `check.md`

## 逐文件验收条件

| 文件 | 验收条件 |
|------|----------|
| `page-map.md` | 每个页面有路径、所属模块、来源范围、关联事实、关联功能或规则 |
| `feature-map.md` | 每个功能有功能说明、来源事实、触发页面、关联规则、关联数据或验收 |
| `rule-map.md` | 每个规则有规则说明、来源事实、触发功能或页面、关联数据对象、关联验收标准 |
| `data-map.md` | 每个数据对象有对象含义、来源事实、关联规则、关键字段或状态字段 |
| `acceptance-map.md` | 每个验收项有验收目标、来源事实、关联规则、验收类型和当前状态 |
| `context-map.md` | 明确呈现事实→页面/功能→规则→数据→验收，以及问题/冲突/推断影响范围 |
| `check.md` | 使用 `03-relate-check-template.md`，并能引用 `check-relate.py` 的检查结果 |

## 检查

使用 `templates/03-relate-check-template.md` 生成 `check.md`。

检查要点：
- 断链检查（每个核心实体都有上下游关联）
- 孤立项检查（无孤立实体）
- 待确认影响检查（问题/冲突/推断关联了影响范围）

## 下一步

通过检查后进入 **Generate（生成）** 阶段。
