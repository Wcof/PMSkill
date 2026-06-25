# ADR 0005: Explicit Inline Markers Replace Soft Gate

## Status

Accepted (2026-06-24)

## Context

The old PRD Helper had a Soft Gate (check) mechanism that ran after each pipeline stage. It never hard-blocked the user but produced separate check reports exposing missing sources, broken relation chains, and pending-confirmation risks. This created a gap: checks could "pass" while risks still existed, and check reports were separate documents that PMs had to cross-reference.

In the new model, PMContext is the sole Entity and is produced through interactive questioning (/pm-refine). The questioning process naturally surfaces ambiguities, conflicts, and assumptions in real-time.

## Decision

Soft Gate / independent check mechanism is removed. Instead, PMContext uses explicit inline markers:

- `[待确认]` — items needing further confirmation
- `[假设]` — Agent inferences without confirmed source
- `[冲突]` — contradictions between sources or statements

Views (PRD/Sketch) faithfully reflect these markers. Items marked `[待确认]` or `[假设]` cannot be written as deterministic implementation requirements.

Traceability is simplified to "sourced / unsourced" (one level): each content item either has an inline source annotation (`← 来源: 某轮追问`) or doesn't. Unsource items are automatically marked `[假设]`.

## Consequences

- No separate check scripts or check report files needed.
- Risk information is always visible inline—no "check passed but risk remains" gap.
- PMs see risks directly in the document they're working with, not in a separate report.
- The old `checks/` directory and `modules/*/scripts/check-*.py` scripts are no longer needed.
- Strong Trace / Weak Trace two-level distinction is eliminated (unsourced items are simply `[假设]`).
