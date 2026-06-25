# ADR 0006: Relate Phase Dispersed Into All Skills

## Status

Accepted (2026-06-24)

## Context

The old PRD Helper had a dedicated Relate stage that built explicit relation chains (fact → page/feature → rule → data/acceptance) and checked for broken chains and orphaned items. This was necessary because entities were scattered across multiple files and directories—explicit chains were needed to connect them.

In the new model, PMContext is a single self-contained file. Relationships are implicit in the heading structure. However, ensuring strong connections between items is still important—PMContext with orphaned items or disconnected facts is low quality.

## Decision

The Relate stage is removed as a separate step. Instead, the discipline of building and maintaining connections is dispersed into every Skill:

- `/pm-collect`: establishes associations between collected materials (same-topic feedback, corroborating or contradictory sources).
- `/pm-refine`: actively builds connections between facts, rules, pages, and acceptance criteria during questioning; ensures PMContext has no orphaned items.
- `/pm-prd`: ensures every requirement traces to a specific item in PMContext; unsourceable requirements are marked `[待确认]`.
- `/pm-sketch`: ensures every diagram element corresponds to an entity/relationship in PMContext; unmappable elements are marked `[假设]`.

## Consequences

- Fewer Skills to maintain (no `/pm-relate` command).
- Connection quality is continuous rather than batch-checked at one stage.
- Each Skill's `_Avoid` list includes disconnection failures (e.g., "沉淀出孤立项不关联", "需求项无追溯", "图元无追溯").
- PMContext heading structure is the primary relationship mechanism; explicit chain notation is no longer used.
