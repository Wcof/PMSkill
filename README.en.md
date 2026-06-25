# PMSkill

A Skill toolkit for product managers working in Agents.

From fuzzy ideas and user requests, distill clear PMContext, then derive deliverable PRD (for AI or human) and sketches (wireframe, IA, state machine, flowchart).

## One-line Value

PMSkill helps product managers working in Agents turn scattered product context — from conversations, meetings, feedback, and old docs — into traceable PMContext through clarifying questions, then derive deliverable PRD and sketches from it.

## Quick Start

### 1. Install

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. Initialize

```text
/pm-setup
```

### 3. Follow the main flow

```text
/pm-need    # collect materials + refine through questions → produce PMContext
/pm-prd     # generate PRD from PMContext (for AI + for human)
/pm-sketch  # generate sketches from PMContext (wireframe/IA/state/flow)
```

## Core Model

**PMContext is the sole Entity (source). PRD and Sketch are its downstream Views.**

- PMContext lands as a single self-contained file `pm-context.md`
- PRD has two forms: for AI (with Agent Context) and for human (review-friendly)
- Sketches use markdown-embedded Mermaid diagrams, readable by Agent
- Risks are marked inline (`[待确认]`/`[假设]`/`[冲突]`), not in separate check reports

## Main Flow

```
Fuzzy ideas / user requests
        ↓
  /pm-need (collect → refine)  →  PMContext (sole Entity)
        ↓                           ↓
  /pm-prd (ai + human)              /pm-sketch (wireframe + ia + state + flow)
        ↓                           ↓
  ai-prd.md + human-prd.md      sketch/*.md (Mermaid diagrams)
```

## Skill List

### Setup — Initialization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-setup` | user-invoked | Configure project (directory/language/Agent rules) |

### Discovery — Requirement Discovery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-need` | user-invoked | Main entry: collect → refine, produce PMContext |
| `/pm-collect` | model-invoked | Collect materials (conversation-first + file import) |
| `/pm-refine` | model-invoked | Clarify through questions (8 dimensions), distill PMContext |

### Delivery — Delivery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-prd` | user-invoked | Output both PRD forms |
| `/pm-aiprd` | model-invoked | Output AI-executable PRD (with Agent Context) |
| `/pm-humanprd` | model-invoked | Output human-readable PRD (review-friendly) |

### Visualization — Visualization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-sketch` | user-invoked | Output all four sketch types |
| `/pm-wireframe` | model-invoked | Wireframe (Mermaid + table) |
| `/pm-ia` | model-invoked | Information architecture (Mermaid graph) |
| `/pm-state` | model-invoked | State machine (Mermaid stateDiagram) |
| `/pm-flow` | model-invoked | Flowchart (Mermaid flowchart) |

## /pm-refine Questioning Dimensions

1. **User scenario**: Who uses it? In what scenario? For what purpose?
2. **Boundary conditions**: What if X fails? What if user does Y simultaneously?
3. **Priority**: Must-have vs nice-to-have? Where is the MVP boundary?
4. **Conflict detection**: When sources contradict, which takes precedence?
5. **Terminology clarification**: What exactly does X mean?
6. **Workaround & friction**: What workaround do users currently use? What's the most painful point?
7. **Tech & resource constraints**: Latency requirements? Token cost? Hardware limits?
8. **Value validation metrics**: What metric proves we did it right? If unchanged, can we remove it?

## Output Directory

```
docs/pm-context/
  pm-context.md          ← Entity (sole)
  collect/               ← /pm-collect organized materials
  prd/
    ai-prd.md            ← AI PRD
    human-prd.md         ← Human PRD
  sketch/
    wireframe.md         ← Wireframe
    ia.md                ← Information architecture
    state.md             ← State machine
    flow.md              ← Flowchart
```

## Design Decisions

Key architectural decisions are recorded in `docs/adr/`:

- **ADR 0004**: PMContext as the sole Entity; PRD and Sketch are Views
- **ADR 0005**: Explicit inline markers replace Soft Gate
- **ADR 0006**: Relate phase dispersed into all Skills
- **ADR 0007**: Single-level traceability replaces Strong/Weak Trace

## FAQ

**Can PMContext be updated?** Yes. PMContext is a living document. Call `/pm-refine` again with new feedback; Agent only questions new parts and incrementally updates.

**Can I skip collect and go straight to refine?** Yes. `/pm-collect` and `/pm-refine` can both be called independently.

**Can I produce only one PRD form?** Yes. `/pm-aiprd` and `/pm-humanprd` can both be called independently.

**Can I produce only one sketch type?** Yes. `/pm-wireframe`, `/pm-ia`, `/pm-state`, `/pm-flow` can all be called independently.

**Do I need /pm-remove?** No. No hooks to clean up, Agent rules are a few lines to delete manually, output directory may have value so not auto-deleted, Skill uninstall is handled by the installer.
