# ADR 0007: Single-Level Traceability Replaces Strong/Weak Trace

## Status

Accepted (2026-06-24)

## Context

The old PRD Helper distinguished Strong Trace (source_id + path + quote/paraphrase + locator) from Weak Trace (only source file, no locator). Only Strong Trace content could become deterministic PRD requirements; Weak Trace was limited to risk/pending sections.

This two-level distinction was necessary because the old model passively imported external materials (meeting notes, old PRDs, customer emails) that often lacked precise locators. The distinction created maintenance burden: every item had to be classified, and the boundary between Strong and Weak was sometimes ambiguous.

## Decision

Traceability is simplified to a single level: "sourced / unsourced".

- Each content item in PMContext either has an inline source annotation (`← 来源: 某轮追问`) or doesn't.
- Items without a source annotation are automatically marked `[假设]`.
- The Strong/Weak Trace two-level distinction is eliminated.

This is justified because PMContext is produced through interactive questioning (/pm-refine), not passive import. Each item's source is almost always "determined in round N of questioning" or "derived from collected material X"—the locator naturally exists. The old pain point (passively imported materials missing locators) is greatly reduced.

## Consequences

- Simpler PMContext format—no need to classify each item's trace level.
- The `source_anchor` module and its Strong/Weak evaluation logic are no longer needed.
- `/pm-collect` still records source metadata (origin, path, hash) in its collected material files, but this is for reference, not for trace-level classification.
- The "unsourced → `[假设]`" rule is enforced by all downstream Skills.
