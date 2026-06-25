# ADR 0004: PMContext as the Sole Entity

## Status

Accepted (2026-06-24)

## Context

The old PRD Helper model had multiple domain entities: Fact, Rule, Page, Feature, Data, Acceptance, each flowing across stages, requiring IDs, and participating in relation chains. This led to a four-stage pipeline (Collect→Refine→Relate→Generate) where each stage produced different entity types, and Relate existed solely to connect them with explicit relation chains.

When repositioning PMSkill for a product manager working in an Agent, the multi-entity model creates two problems: (1) PMs think in terms of one coherent product context, not scattered entity types; (2) the pipeline structure forces a rigid stage order that doesn't match how PMs actually work—they iterate, jump back, and incrementally refine.

## Decision

PMContext is the sole Entity in the new model. It is the source from which all PRD and Sketch Views derive. PRD and Sketch are Views (downstream expressions), not Entities.

- PMContext lands as a single self-contained file `pm-context.md`, using headings for structure.
- The old four-stage pipeline is replaced by: `/pm-need` (collect → refine to produce PMContext) → `/pm-prd` → `/pm-sketch`.
- Relationships are implicit in the heading structure of PMContext, not maintained as explicit relation chains.

## Consequences

- Simpler mental model: PMs work with one living document, not a pipeline of stage outputs.
- No need for a dedicated Relate stage (see ADR 0006).
- The heading structure of PMContext must be well-designed, since it replaces explicit relation chains.
- Old modules (`modules/collect/`, `modules/refine/`, `modules/relate/`, `modules/generate/`) are replaced by new Skill structure.
- PMContext is a living document that supports incremental updates (see ADR 0005 implications).
