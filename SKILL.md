---
name: prd-helper
description: PRD Helper local entry. Initialize or repair PRD Helper and expose the traceable PRD Context Compiler workflow for local Claude, Codex, and Trae installs.
allowed-tools: Bash, Read
---

# PRD Helper Local Entry

This root `SKILL.md` is the local-install entry for users who download or clone this repository and ask Claude, Codex, or Trae to install/use it directly.

PRD Helper is a **PRD Context Compiler**, not an automatic PRD writer. It compiles product context through:

1. Collect
2. Refine
3. Relate
4. Generate

Check is a Soft Gate across the workflow, not a fifth business stage. Generated documents are Views, not domain Entities. Only objects that flow across stages, need IDs, need references, and participate in relation chains are Entities. Strong Trace requires `source_id + path + quote/paraphrase + locator`; Weak Trace cannot become deterministic implementation requirements.

## Activation

When the user invokes this local Skill, initialize or repair the current project:

```bash
python3 scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent codex
python3 scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
```

Use the agent that matches the current runtime. For Trae, use `--agent trae`.

After initialization, use the command Skills in `skills/prd-*/SKILL.md`:

- `/prd-helper`
- `/prd-start`
- `/prd-stop`
- `/prd-status`
- `/prd-scan`
- `/prd-import`
- `/prd-refine`
- `/prd-relate`
- `/prd-generate`
- `/prd-discuss`
- `/prd-remove`

The detailed workflow rules live in `skills/prd-helper/SKILL.md`, `modules/*/guide.md`, and `checks/guide.md`.

## Installer Note

Because this root entry exists for local direct installation, `npx skills@latest add Wcof/PRDContextEngine` should use full-depth discovery when installing the complete command package:

```bash
npx skills@latest add Wcof/PRDContextEngine --all --full-depth
```

