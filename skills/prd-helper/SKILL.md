---
name: prd-helper
description: Use this skill when transforming product discussions, meeting notes, prototype notes, customer feedback, review notes, or agent session summaries into structured PRD documents through collect, refine, relate, and generate steps.
---

# PRD Helper Skill

You are helping the user process product requirement context.

Do not directly generate final PRD documents from raw input.

Always follow the four product workflow steps:

1. Collect
2. Refine
3. Relate
4. Generate

Checks are required after every step.

## Core Rule

The four business modules are:

- collect
- refine
- relate
- generate

Check is a required quality gate across every module, not a fifth business step.

## When to Use

Use this skill when the user provides:

- product discussions
- meeting notes
- customer feedback
- prototype notes
- agent session summaries
- requirement drafts
- page descriptions
- PRD fragments
- review notes
- legacy documents

## Required Behavior

- Preserve source context
- Separate facts from assumptions
- Mark conflicts
- Mark open questions
- Build relations between facts, pages, features, rules, data, and acceptance
- Generate role-specific PRD documents
- Run checks after each step
- Output Context Delta at the end

## Workflow

### Step 1: Collect

Save raw input to `docs/prd-helper/01-collect/`.

Each source file must include material title, material type, source, recording time, recorder, owner, priority, raw content, related modules, and keywords.

After collecting, run collect check and output `01-collect/check.md`.

### Step 2: Refine

Extract from collected materials into `docs/prd-helper/02-refine/`:

- `facts.md` - requirement facts
- `background.md` - business background
- `goals.md` - business goals
- `decisions.md` - design decisions
- `constraints.md` - business constraints
- `conflicts.md` - conflict points
- `questions.md` - open questions
- `assumptions.md` - AI inferences

Critical rule: NEVER write AI inferences as confirmed facts.

After refining, run refine check and output `02-refine/check.md`.

### Step 3: Relate

Build relations in `docs/prd-helper/03-relate/`:

- `page-map.md` - fact to page relations
- `feature-map.md` - feature to rule relations
- `rule-map.md` - rule to data relations
- `data-map.md` - data object relations
- `acceptance-map.md` - acceptance criteria relations
- `context-map.md` - overall context relations

After relating, run relate check and output `03-relate/check.md`.

### Step 4: Generate

Generate structured documents in `docs/prd-helper/04-generate/`:

- `overview/project-overview.md`
- `pages/` - page specifications
- `rules/` - business rules
- `data/` - data specifications
- `acceptance/` - acceptance criteria
- `agent-context/` - role-specific agent contexts (frontend, backend, test, product)

After generating, run generate check and output `04-generate/check.md`.

### Final Check

Check is not a fifth business module. After the four workflow steps are complete, run final check in `docs/prd-helper/05-check/`:

- `full-check.md` - overall completeness check
- `gap-check.md` - gap analysis
- `relation-check.md` - relation integrity check
- `source-check.md` - source traceability check
- `generated-check.md` - generated content check
- `context-delta.md` - context delta for this session

## References

Read these files when needed:

- references/workflow.md
- references/collect.md
- references/refine.md
- references/relate.md
- references/generate.md
- references/check-rules.md
- references/context-delta.md

## Templates

Use templates from:

- assets/templates/
