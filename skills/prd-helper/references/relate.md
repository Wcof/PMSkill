# 关联环节（Relate）

## 目标

关联环节负责把精炼后的需求上下文与实际产品结构建立关系。

这是 PRD Helper 区别于普通 PRD 生成器的关键环节。

核心目标：让需求、页面、功能、规则、数据和验收之间不断链。

## 关联对象

关联环节需要建立以下关系：

1. 需求事实 → 页面
2. 需求事实 → 功能
3. 功能 → 业务规则
4. 业务规则 → 数据对象
5. 页面 → 字段
6. 页面 → 操作
7. 页面 → 状态
8. 页面 → 接口用途
9. 页面 → 验收标准
10. 规则 → 异常场景
11. 待确认问题 → 影响范围
12. 冲突点 → 影响范围
13. AI 推断项 → 影响范围
14. Agent 对话 → 相关文档

## 输出目录

```
docs/prd-helper/03-relate/
```

## 输出文件

| 文件 | 用途 | 模板 |
|------|------|------|
| `page-map.md` | 页面关联图 | `03-relate-page-map-template.md` |
| `feature-map.md` | 功能关联图 | `03-relate-feature-map-template.md` |
| `rule-map.md` | 规则关联图 | `03-relate-rule-map-template.md` |
| `data-map.md` | 数据关联图 | `03-relate-data-map-template.md` |
| `acceptance-map.md` | 验收关联图 | `03-relate-acceptance-map-template.md` |
| `context-map.md` | 上下文总关联图 | `03-relate-context-map-template.md` |
| `check.md` | 关联检查 | `03-relate-check-template.md` |

## 行为规范

1. 每个需求事实必须关联到页面或功能。
2. 每个功能必须关联到业务规则。
3. 每个业务规则必须关联到数据对象。
4. 每个页面必须关联到验收标准。
5. 待确认问题必须关联影响范围。
6. 冲突点必须关联影响范围。
7. AI 推断项必须关联影响范围。
8. 不允许存在孤立需求、孤立页面、孤立规则。

## 验收标准

关联环节完成必须满足：

1. 有 page-map。
2. 有 feature-map。
3. 有 rule-map。
4. 有 data-map。
5. 有 acceptance-map。
6. 有 context-map。
7. 能看出需求到页面、功能、规则、数据、验收的链路。
8. 待确认问题有影响范围。
9. 冲突点有影响范围。
10. 生成 `check.md`。
