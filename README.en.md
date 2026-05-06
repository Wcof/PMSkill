# PRD Helper

[中文](README.md) | [English](README.en.md)

![PRD Helper project overview](support/assets/prd-helper-project-overview.svg)

## One-line Value

PRD Helper turns product context scattered across meetings, chats, reviews, and legacy documents into traceable, checkable, reusable structured PRD assets.

## What Problem It Solves

Many teams do not lack requirement material. The problem is that the material is scattered, source evidence is unclear, and versions drift. PRD Helper keeps the workflow disciplined: collect raw input first, refine it, relate it, then generate PRD documents instead of asking AI to guess from fragmented conversations.

## Core Capabilities

| Feature | Purpose | Problem Solved |
|---|---|---|
| `/prd-helper` project setup | Creates config, folders, and follow-up commands | The project is installed but not ready |
| `/prd-start` active capture | Starts recording product discussions | Important context gets lost |
| Pause/resume/stop capture | Controls capture boundaries and hook state | Accidental or unclear capture scope |
| `/prd-scan` batch scan | Imports historical Agent sessions | Existing context is disconnected |
| Passive intake folder | Stores meeting notes, old PRDs, customer feedback | Non-chat materials are unmanaged |
| Four-module workflow | Collect -> Refine -> Relate -> Generate | Direct PRD generation causes omissions |
| Check scripts | Validates each stage | Outputs are not auditable |
| `/prd-grill` mode | Challenges vague terms and contradictions | Ambiguous language and weak decisions |
| `/prd-remove` uninstall | Cleans commands, configs, and hooks | Installation leftovers pollute the project |

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

### 3. Use Capture Commands

```text
/prd-start   # Start active capture
/prd-pause   # Pause active capture and clean hooks
/prd-resume  # Resume active capture
/prd-stop    # Stop capture and generate summary/check output
/prd-status  # Show current capture state
/prd-scan    # Scan historical Agent sessions into the capture pool
/prd-grill   # Challenge contradictions and ambiguous concepts
/prd-remove  # Uninstall PRD Helper and clean project config
```

Active capture output goes to:

```text
docs/prd-helper/01-collect/active/
```

Passive materials go to:

```text
docs/prd-helper/01-collect/passive/
```

## Four-module Workflow

| Module | Directory | Output Goal |
|---|---|---|
| Collect | `modules/collect/` | Preserve raw materials, build indexes, lightly mark noise |
| Refine | `modules/refine/` | Extract facts, decisions, constraints, questions, assumptions |
| Relate | `modules/relate/` | Connect facts, pages, rules, data, and acceptance criteria |
| Generate | `modules/generate/` | Produce PRD context for product, engineering, and QA |

## Check Commands

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

Want to uninstall: run `/prd-remove`. It cleans project config, commands, and hooks while keeping existing `docs/prd-helper/` documents by default.

## Open-source Governance

- Contributing: `CONTRIBUTING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`
- Security Policy: `SECURITY.md`
- Support: `SUPPORT.md`
- Changelog: `CHANGELOG.md`
- GitHub cover prompt guide: `docs/github-project-kit.md`
