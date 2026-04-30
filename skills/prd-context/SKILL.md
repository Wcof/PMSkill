---
name: prd-context
description: Use this skill when turning product discussions, meeting notes, prototype notes, customer feedback, or agent conversation summaries into structured PRD context through collect, refine, relate, generate, and check steps.
---

# PRD Context Skill

You are helping the user process product requirement context for PRD helper.

Do not directly generate a final PRD from raw input.

Always follow this workflow:

1. Collect
2. Refine
3. Relate
4. Generate
5. Check

## Core Rule

The four product modules are:

- collect
- refine
- relate
- generate

The check process is a required quality gate across every module.

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

## Required Behavior

- Preserve source context
- Separate facts from assumptions
- Mark conflicts and open questions
- Build relations between facts, pages, features, rules, data, and acceptance
- Generate role-specific PRD context
- Run checks after each step
- Output Context Delta at the end

## Workflow

### Step 1: Collect

Save raw input to `docs/prd-context/01-sources/`.

Each source file must include:
- material title
- material type
- source
- recording time
- recorder
- raw content
- related modules
- keywords
- whether refinement is needed

After collecting, run collect check and output `01-sources/check.md`.

### Step 2: Refine

Extract from sources into `docs/prd-context/02-refined/`:

- `facts.md` - requirement facts
- `decisions.md` - design decisions
- `constraints.md` - business constraints
- `conflicts.md` - conflict points
- `questions.md` - open questions
- `assumptions.md` - AI inferences

Critical rule: NEVER write AI inferences as confirmed facts.

After refining, run refine check and output `02-refined/check.md`.

### Step 3: Relate

Build relations in `docs/prd-context/03-relations/`:

- `page-map.md` - fact → page relations
- `feature-map.md` - feature → rule relations
- `rule-map.md` - rule → data relations
- `data-map.md` - data object relations
- `acceptance-map.md` - acceptance criteria relations
- `context-map.md` - context change relations

After relating, run relate check and output `03-relations/check.md`.

### Step 4: Generate

Generate structured documents in `docs/prd-context/04-generated/`:

- `overview/project-overview.md`
- `pages/` - page specifications
- `rules/` - business rules
- `data/` - data specifications
- `acceptance/` - acceptance criteria
- `agent-context/` - role-specific agent contexts (frontend, backend, test, product)

After generating, run generate check and output `04-generated/check.md`.

### Step 5: Check

Run final check in `docs/prd-context/05-check/`:

- `full-check.md` - overall completeness check
- `gap-check.md` - gap analysis
- `relation-check.md` - relation integrity check
- `generated-check.md` - generated content check
- `context-delta.md` - context delta for this session
- `next-actions.md` - recommended next steps

## References

Read these files when needed:

- references/workflow.md
- references/check-rules.md
- references/output-rules.md
- references/context-delta.md

## Templates

Use templates from:

- assets/templates/
