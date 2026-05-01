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

## Workflow

### Step 1: Collect

Read `modules/collect/guide.md` and use templates in `modules/collect/templates/`.

Save raw input to `docs/prd-helper/01-collect/`.

After collecting, run collect check and output `01-collect/check.md`.

### Step 2: Refine

Read `modules/refine/guide.md` and use templates in `modules/refine/templates/`.

Extract structured information to `docs/prd-helper/02-refine/`.

After refining, run refine check and output `02-refine/check.md`.

### Step 3: Relate

Read `modules/relate/guide.md` and use templates in `modules/relate/templates/`.

Build relations in `docs/prd-helper/03-relate/`.

After relating, run relate check and output `03-relate/check.md`.

### Step 4: Generate

Read `modules/generate/guide.md` and use templates in `modules/generate/templates/`.

Generate structured documents in `docs/prd-helper/04-generate/`.

After generating, run generate check and output `04-generate/check.md`.

### Final Check

Read `checks/guide.md` and use templates in `checks/templates/`.

Final check output goes to `docs/prd-helper/05-check/`, including `context-delta.md`.
