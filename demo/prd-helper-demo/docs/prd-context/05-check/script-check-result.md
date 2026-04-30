# Script Check Report

## Summary

All 3 check scripts passed.

| Script | Result |
|--------|--------|
| check-structure.py | PASS (38/38) |
| check-relations.py | PASS (12/12 facts covered) |
| check-generated.py | PASS (no unresolved content) |

---

## 1. Structure Check (check-structure.py)

| Metric | Count |
|--------|-------|
| Total | 38 |
| Pass | 38 |
| Fail | 0 |

| Type | Path | Status |
|------|------|--------|
| directory | 01-sources | PASS |
| directory | 02-refined | PASS |
| directory | 03-relations | PASS |
| directory | 04-generated | PASS |
| directory | 05-check | PASS |
| file | 01-sources/check.md | PASS |
| file | 02-refined/facts.md | PASS |
| file | 02-refined/decisions.md | PASS |
| file | 02-refined/constraints.md | PASS |
| file | 02-refined/conflicts.md | PASS |
| file | 02-refined/questions.md | PASS |
| file | 02-refined/assumptions.md | PASS |
| file | 02-refined/check.md | PASS |
| file | 03-relations/page-map.md | PASS |
| file | 03-relations/feature-map.md | PASS |
| file | 03-relations/rule-map.md | PASS |
| file | 03-relations/data-map.md | PASS |
| file | 03-relations/acceptance-map.md | PASS |
| file | 03-relations/context-map.md | PASS |
| file | 03-relations/check.md | PASS |
| file | 04-generated/check.md | PASS |
| file | 05-check/full-check.md | PASS |
| file | 05-check/gap-check.md | PASS |
| file | 05-check/relation-check.md | PASS |
| file | 05-check/generated-check.md | PASS |
| file | 05-check/context-delta.md | PASS |
| file | 05-check/next-actions.md | PASS |
| directory | 04-generated/overview | PASS |
| directory | 04-generated/pages | PASS |
| directory | 04-generated/rules | PASS |
| directory | 04-generated/data | PASS |
| directory | 04-generated/acceptance | PASS |
| directory | 04-generated/agent-context | PASS |
| file | 04-generated/overview/project-overview.md | PASS |
| file | 04-generated/agent-context/frontend-context.md | PASS |
| file | 04-generated/agent-context/backend-context.md | PASS |
| file | 04-generated/agent-context/test-context.md | PASS |
| file | 04-generated/agent-context/product-review-context.md | PASS |

---

## 2. Relation Check (check-relations.py)

### Facts

- Total facts: 12
- With source: 12
- With status: 12

### Relations

| File | Entries | Status |
|------|---------|--------|
| page-map.md | 7 | PASS |
| feature-map.md | 10 | PASS |
| rule-map.md | 6 | PASS |
| data-map.md | 14 | PASS |
| acceptance-map.md | 7 | PASS |

### Fact Coverage

- Total facts: 12
- Mapped to pages/features: 12
- Status: All facts mapped

### Isolation Check

- No isolated items found

---

## 3. Generated Content Check (check-generated.py)

### Structure

| Check | Status |
|-------|--------|
| 04-generated/overview exists | PASS |
| 04-generated/overview/project-overview.md exists | PASS |
| 04-generated/pages exists | PASS |
| 04-generated/pages has content | PASS (1 file) |
| 04-generated/rules exists | PASS |
| 04-generated/rules has content | PASS (1 file) |
| 04-generated/data exists | PASS |
| 04-generated/data has content | PASS (1 file) |
| 04-generated/acceptance exists | PASS |
| 04-generated/acceptance has content | PASS (1 file) |
| 04-generated/agent-context exists | PASS |
| 04-generated/agent-context/frontend-context.md exists | PASS |
| 04-generated/agent-context/backend-context.md exists | PASS |
| 04-generated/agent-context/test-context.md exists | PASS |
| 04-generated/agent-context/product-review-context.md exists | PASS |

### Unresolved Content

- No unresolved content found

### Page Completeness

- prd-helper-context-processing.md: PASS (all required sections present)

### Rule Completeness

- context-refine-relation-rule.md: PASS (all required sections present)
