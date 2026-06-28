# PMSkill

A Skill toolkit for product managers working in Agents.

From fuzzy ideas/user requests, **one-command full pipeline** distills PMContext → derives PRD (for AI + for human) → generates visual sketches + interactive HTML prototype.

> Optimized through 9 rounds of darwin-skill structural optimization + best practices from [pm-skills (PM Compass)](https://github.com/phuryn/pm-skills). All 13 SKILL.md files cover role setup, output examples, further references, and practical tips. Compliant with [Anthropic Agent Skills specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): YAML frontmatter progressive disclosure, third-person trigger descriptions, Level 3 references loaded on demand.

## One-line Value

PMSkill helps product managers working in Agents turn scattered, fuzzy product context into traceable PMContext through a **zero-confirmation automatic pipeline**, then derive deliverable PRD and sketches from it.

## Quick Start

### 1. Install

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. Initialize (once)

```text
/pm-setup
```

### 3. One-command full pipeline (recommended)

One sentence triggers collect → refine → PRD → prototype, zero confirmation:

```text
/pm-need <requirement description> --auto
```

Example: `/pm-need membership system redesign --auto`

### 4. Step-by-step

```text
/pm-need              # Auto-collect materials + infer clarification → produce PMContext, pause at audit gate
/pm-prd               # Generate PRD from PMContext (for AI + for human)
/pm-prd --auto        # Zero-confirmation mode: produce PRD directly, no pause
/pm-sketch            # Generate all sketches from PMContext
/pm-sketch --prototype # Generate Mermaid sketches + interactive HTML prototype
```

## Core Model

**PMContext is the sole Entity (source). PRD and Sketch are its downstream Views.**

- PMContext lands as a single self-contained file `pm-context.md`; downstream Skills read one file to know the full picture
- PRD has two forms: for AI (with Agent Context, directly executable) and for human (review-friendly)
- Sketches use markdown-embedded Mermaid diagrams, readable by Agent
- HTML prototype (`--prototype`) is a single page with no external dependencies, works offline, 9-point quality check
- Risks are marked inline (`[待确认]`/`[假设]`/`[冲突]`), not in separate check reports

## Main Flow

```
Fuzzy ideas / user requests
        │
  /pm-need ─── {--auto: zero-confirm} ───→ PMContext (sole Entity)
        │                                   │
  ┌─────┴─────┐                    ┌────────┴────────┐
  │           │                    │                 │
/pm-prd    /pm-premortem     /pm-sketch          /pm-sketch --prototype
  │           │                    │                 │
  ▼           ▼                    ▼                 ▼
prd/*.md   premortem.md      sketch/*.md       prototype.html
```

## Skill List

### Setup — Initialization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-setup` | user-invoked | First-time project config (output dir/language/knowledge base/Agent rules) |

### Discovery — Requirement Discovery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-need` | user-invoked | 🏆 Main entry: collect → refine → audit, all automatic. `--auto` zero-confirm straight to PRD+prototype |
| `/pm-collect` | model-invoked | Deep scan (code/git/URL/knowledge base), 4 sources deduplicated, **no filtering, only organizing** |
| `/pm-refine` | model-invoked | 8-dimension autonomous inference (P0 user scenarios/boundaries/conflicts → P1 priority/terminology/friction → P2 tech constraints/metrics), with confidence levels |

### Delivery — Delivery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-prd` | user-invoked | Orchestrate dual-form PRD output. `--auto` zero-confirm, `--skip-ai`/`--skip-human` optional |
| `/pm-aiprd` | model-invoked | AI PRD: executable rules + data model + Agent Context + acceptance criteria + risk items |
| `/pm-humanprd` | model-invoked | Human PRD: decision rationale + narrative + traceability list, review-friendly |
| `/pm-premortem` | model-invoked | Pre-Mortem risk analysis: Tiger (real risk) / Paper Tiger (over-concern) / Elephant (undiscussed) + action plan |

### Visualization — Visualization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-sketch` | user-invoked | 🏆 Main entry: output all four sketch types + HTML prototype (`--prototype`). `--auto` zero-confirm |
| `/pm-wireframe` | model-invoked | Wireframe: Mermaid page navigation + Markdown table component layout |
| `/pm-ia` | model-invoked | Information architecture: Mermaid graph, entities/pages + navigation/containment/reference edges |
| `/pm-state` | model-invoked | State machine: Mermaid stateDiagram-v2, states + transition conditions + error paths |
| `/pm-flow` | model-invoked | Flowchart: Mermaid flowchart, steps + decisions + errors, loops with exit conditions |

## Skill Invocation Rules

- **user-invoked**: Only triggered by humans (`disable-model-invocation: true`), can invoke model-invoked sub-skills
- **model-invoked**: Can be triggered autonomously by Agent or orchestrated by user-invoked skills
- user-invoked **cannot** invoke another user-invoked skill

## Zero-confirmation Mode (--auto)

All user-invoked skills support the `--auto` flag:

```text
/pm-need <requirement> --auto        # Full pipeline: collect → refine → PRD → prototype, zero-confirm
/pm-prd --auto                       # Generate PRD from existing PMContext directly, no pause
/pm-sketch --auto                    # Generate all sketches + HTML prototype directly
```

Under `--auto` mode:
- No waiting for PM confirmation; all outputs land immediately
- Sub-skill failures don't block the pipeline; failed items are flagged individually
- One-stop report with confidence distribution + information gaps for post-hoc audit

## /pm-refine Inference Dimensions (8 dimensions full coverage)

```
P0 (must infer first):
1. User scenarios    2. Boundary conditions    3. Conflict detection

P1 (determines quality ceiling):
4. Priority (ICE/RICE/Kano)    5. Terminology clarification    6. Workaround & friction

P2 (incremental enhancement):
7. Tech & resource constraints    8. Value validation metrics
```

## Failure Mode Handling

All Skills use a uniform **three-column fallback table** (trigger condition → first-line fix → still-fails fallback):

| Trigger Condition | First-line Fix | Still-fails Fallback |
|---|---|---|
| PMContext does not exist | 🔴 STOP: prompt to run `/pm-need` first | Non-blocking, exit after prompt |
| Sub-skill generation fails | Don't block main flow; flag failed item | Other successful parts still land |
| Materials/info insufficient | 🟡 WARNING mark in info gaps + lower confidence | Don't fabricate; continue processing |

## Output Directory

```
docs/pm-context/
  pm-context.md          ← Sole Entity (source)
  collect/               ← /pm-collect organized raw materials
  prd/
    ai-prd.md            ← AI PRD (Agent-executable)
    human-prd.md         ← Human PRD (review-friendly)
  sketch/
    wireframe.md         ← Wireframe (Mermaid + table)
    ia.md                ← Information architecture (Mermaid graph)
    state.md             ← State machine (Mermaid stateDiagram-v2)
    flow.md              ← Flowchart (Mermaid flowchart)
    prototype.html       ← Interactive HTML prototype (--prototype mode)
```

## Project Structure

```
PMSkill/
├── INSTALL.md                    ← Local direct-install entry (not a Skill, no frontmatter)
├── CLAUDE.md                     ← Agent instructions + project-level Skill rules
├── CONTEXT.md                    ← Domain glossary
├── README.md                     ← This file
├── .claude-plugin/plugin.json    ← Claude Code plugin manifest
├── .codex-plugin/plugin.json     ← Codex plugin manifest
├── skills/
│   ├── setup/
│   │   ├── README.md             ← Bucket navigation
│   │   └── pm-setup/
│   │       ├── SKILL.md          ← Level 1+2 progressive disclosure
│   │       └── references/       ← Level 3 loaded on demand
│   ├── discovery/
│   │   ├── README.md
│   │   ├── pm-need/SKILL.md + references/
│   │   ├── pm-collect/SKILL.md + references/
│   │   └── pm-refine/SKILL.md
│   ├── delivery/
│   │   ├── README.md
│   │   ├── pm-prd/SKILL.md
│   │   ├── pm-aiprd/SKILL.md
│   │   ├── pm-humanprd/SKILL.md
│   │   └── pm-premortem/SKILL.md
│   └── visualization/
│       ├── README.md
│       ├── pm-sketch/SKILL.md + references/
│       ├── pm-wireframe/SKILL.md
│       ├── pm-ia/SKILL.md
│       ├── pm-state/SKILL.md
│       └── pm-flow/SKILL.md
└── docs/
    └── adr/                      ← Architecture Decision Records
```

## Progressive Disclosure

This project follows the [Anthropic Agent Skills three-level progressive disclosure specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):

| Level | When Loaded | Token Cost | Content |
|---|---|---|---|
| Level 1: Metadata | Always (at startup) | ~100 tokens/skill | YAML frontmatter `name` + `description` |
| Level 2: Instructions | When Skill is triggered | < 5k tokens | SKILL.md body (workflow/failure modes/anti-pattern blacklist) |
| Level 3: Resources | As referenced | Unlimited | `references/` with output examples, further references, practical tips |

## Further References

Inspired by:

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [PM Skills Marketplace (68 PM skills)](https://github.com/phuryn/pm-skills)
- [Continuous Discovery Habits - Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [A Proven AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Mermaid Official Docs](https://mermaid.js.org/)
- [Pre-Mortem: Meta/Instagram Practice](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [Anthropic Agent Skills Specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Design Decisions

Key architectural decisions (recorded in `docs/adr/`, visible in development, not included in install package):

- **ADR 0004**: PMContext is the sole Entity; PRD and Sketch are Views
- **ADR 0005**: Explicit inline markers replace Soft Gate; risks written in body
- **ADR 0006**: Relate phase dispersed into all Skills; association is built-in discipline
- **ADR 0007**: Single-level traceability (sourced/unsourced) replaces Strong/Weak Trace

## FAQ

**Can PMContext be updated?** Yes. PMContext is a living document. Call `/pm-refine` again with new feedback; Agent only infers new parts and incrementally updates.

**Can I skip collect and go straight to refine?** Yes. `/pm-collect` and `/pm-refine` can both be called independently.

**Can I produce only one PRD form / one sketch type?** Yes. All sub-skills can be called independently.

**What's the difference between --auto and normal mode?** Normal mode pauses at the audit gate after producing PMContext for PM confirmation; `--auto` mode doesn't wait, lands everything in one pass, and produces a one-stop report for post-hoc audit.

**Do I need /pm-remove?** No. No hooks to clean up, Agent rules are a few lines to delete manually, output directory may have value so not auto-deleted.

**Which Agents are supported?** All skills-compatible runtimes: Claude Code, Codex, Cursor, Trae, OpenClaw, Hermes, etc. Install command auto-adapts; no manual path specification needed.
