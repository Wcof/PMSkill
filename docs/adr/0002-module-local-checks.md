# ADR 0002: Module-Local Check Scripts

## Status

Accepted

## Context

早期 `check-relations.py` 同时检查采集元信息、精炼可追溯性和关联覆盖度，导致脚本名称与职责不一致，也让调用方需要理解跨模块依赖。

## Decision

每个业务模块拥有自己的检查入口：

- `check-collect.py` 检查 `01-collect/`
- `check-refine.py` 检查 `02-refine/`
- `check-relate.py` 检查 `03-relate/`
- `check-generated.py` 检查 `04-generate/`

`check-relations.py` 仅保留为兼容旧流程的薄包装。

## Consequences

- 检查问题定位更清楚。
- 每个脚本输出对应模块的 `check.md`。
- 后续新增检查规则时优先放入对应模块脚本，不再扩展上帝脚本。
