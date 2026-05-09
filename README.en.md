# PRD Helper

[中文](README.md) | [English](README.en.md)

![PRD Helper project overview](support/assets/prd-helper-project-overview.svg)

## One-line Value

PRD Helper is a **PRD Context Compiler**: it turns product context scattered across meetings, chats, reviews, and legacy documents into traceable, checkable, reusable structured PRD assets and **Agent Context** engineering guidance.

It follows one main chain: **Collect -> Refine -> Relate -> Generate**. Check is a horizontal **Soft Gate**, not a fifth stage. A Soft Gate does not hard-block user commands by default; it exposes missing sources, broken relation chains, and pending-confirmation risks.

## What Problem It Solves

Many teams do not lack requirement material. The problem is that the material is scattered, source evidence is unclear, and versions drift. PRD Helper keeps the workflow disciplined: collect raw input first, refine it, relate it, then generate PRD documents and Agent Context that guide humans or Agents through implementation instead of asking AI to guess from fragmented conversations.

If the user skips prerequisite stages or checks do not pass, `/prd-generate` still runs, but the result is **Limited Generate**: missing sources, broken relation chains, pending questions, and prohibited implementation items must be explicit and cannot be presented as a complete deterministic PRD.

Generated documents are **Views**, not an **Entity** type. Only objects that flow across stages, need references, need IDs, and participate in relation chains are domain entities. Traceability is also graded: content with `source_id + path + quote/paraphrase + locator` is **Strong Trace**; content without a locator is **Weak Trace** and cannot become a deterministic requirement.

## Current Commands

The authoritative command set is cross-checked against `scripts/lib/constants.py`, `commands/*.md`, `SKILL.md`, and plugin manifests. README now documents these 11 commands:

| Command | Stage/Type | Purpose | Main Outputs |
|---|---|---|---|
| `/prd-helper` | Setup entry | Initialize or repair project config, `docs/prd-helper/`, and project commands | Config, folders, Agent rules |
| `/prd-start` | Collect | Start active capture for upcoming product discussion | `01-collect/active/`, `collect-state.md` |
| `/prd-stop` | Collect | Stop active capture, clean hooks, and write summary/check output | `collect-summary.md`, `01-collect/check.md` |
| `/prd-status` | Collect utility | Show capture state, session, write roots, and counts | Status summary |
| `/prd-scan` | Collect utility | Scan historical Agent sessions into the capture pool | `01-collect/active/historical/`, `source-index.md` |
| `/prd-import` | Collect utility | Import a third-party folder as passive material without rewriting raw content | `01-collect/passive/`, `source-index.md` |
| `/prd-refine` | Refine | Extract facts, background, goals, decisions, constraints, conflicts, questions, and assumptions | `02-refine/` |
| `/prd-relate` | Relate | Build upstream/downstream links across facts, pages, features, rules, data, and acceptance | `03-relate/` |
| `/prd-generate` | Generate | Generate PRD docs and Agent context from refined and related outputs | `04-generate/` |
| `/prd-discuss` | Auxiliary discussion | Ask one question at a time about contradictions, vague terms, and unresolved issues | Discussion summary, open questions |
| `/prd-remove` | Uninstall | Clean project config, commands, and hooks while preserving generated docs by default | Cleanup result |

Platform note: the Claude Code plugin manifest includes all 11 commands. `COMMAND_NAMES` contains the 10 generated follow-up commands; `/prd-helper` is the root Skill entry.

## Engineering Constraints

PRD Helper keeps Python as the executor and static prompts/templates as the constraint layer:

- Command facts live in `scripts/lib/command_registry.py`; `COMMAND_NAMES`, setup scripts, and consistency tests derive from it.
- Business rules stay in `SKILL.md`, `modules/*/guide.md`, and `commands/*.md`; Python does not act as the prompt source.
- Output structures and checklists live in `modules/*/templates/`; scripts only fill state, counts, check results, and source details.

## Quick Start

### 1. Install the Skill

```bash
npx skills@latest add Wcof/PRDContextEngine
```

Use `↑/↓` to move, `Space` to select, and `Enter` to confirm. Select `prd-helper` and the target Agent, such as Claude Code or Codex.

### 2. Initialize the Current Project

Run this in your Agent session:

```text
/prd-helper
```

Initialization creates the default docs root `docs/prd-helper/` and generates follow-up commands.

### 3. Follow the Four Stages

```text
/prd-start    # Start active capture
/prd-stop     # Stop active capture and write summary output
/prd-scan     # Scan historical Agent sessions
/prd-import   # Import a third-party folder as passive material
/prd-refine   # Refine collected materials
/prd-relate   # Build upstream/downstream relation chains
/prd-generate # Generate PRD docs and Agent context
```

Use `/prd-status` to inspect state, `/prd-discuss` to clarify ambiguity, and `/prd-remove` to uninstall.

Active capture output goes to:

```text
docs/prd-helper/01-collect/active/
```

Passive materials go to:

```text
docs/prd-helper/01-collect/passive/
```

## Four-stage Workflow

| Stage | Directory | Does | Does Not |
|---|---|---|---|
| Collect | `modules/collect/` | Preserve raw materials, build indexes, record hashes, maintain capture state | Rewrite facts early or generate rules |
| Refine | `modules/refine/` | Separate facts, background, goals, decisions, constraints, conflicts, questions, assumptions | Turn assumptions into facts or jump to PRD |
| Relate | `modules/relate/` | Build `fact -> page/feature -> rule -> data/acceptance` chains | Leave facts, rules, data, or acceptance disconnected |
| Generate | `modules/generate/` | Produce PRD, acceptance, data docs, and Agent context | Add unsourced or unrelated business rules |

## Check Commands

These are script-level quality gates, not slash commands:

```bash
python3 modules/collect/scripts/check-collect.py --root docs/prd-helper/01-collect
python3 modules/refine/scripts/check-refine.py docs/prd-helper
python3 modules/relate/scripts/check-relate.py docs/prd-helper
python3 modules/generate/scripts/check-generated.py docs/prd-helper
python3 scripts/check-structure.py docs/prd-helper
```

## FAQ

Only `/prd-helper` appears, not `/prd-start`: run `/prd-helper` once to initialize project commands. Claude Code may need a new session to refresh command discovery.

No capture output: run `/prd-status` and confirm the state is `on`; then inspect `docs/prd-helper/01-collect/collect-state.md`.

Not sure whether to use `/prd-scan` or `/prd-import`: use `/prd-scan` for historical Agent sessions; use `/prd-import` or `01-collect/passive/` for third-party folders, meeting notes, legacy PRDs, and customer feedback.

Want to uninstall: run `/prd-remove`. It cleans project config, commands, and hooks while keeping existing `docs/prd-helper/` documents by default.

## Open-source Governance

- Contributing: `CONTRIBUTING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`
- Security Policy: `SECURITY.md`
- Support: `SUPPORT.md`
- Changelog: `CHANGELOG.md`
- GitHub cover prompt guide: `docs/github-project-kit.md`
