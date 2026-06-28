# PMSkill Local Entry

This `INSTALL.md` is the local direct-install fallback for users who download or clone this repository and ask Claude, Codex, or Trae to install/use it directly without `npx`.

It intentionally is not a Skill (no YAML frontmatter) and won't be picked up by skill loaders. `npx skills@latest add Wcof/PMSkill` should discover the grouped command Skills under `skills/*/SKILL.md`; this file is only for natural-language loading by an Agent reading the repo root.

PMSkill is a **product manager's Skill toolkit for working in Agents**. It turns fuzzy ideas and user requests into traceable PMContext, then derives deliverable PRD (for AI or human) and sketches (wireframe, IA, state machine, flowchart).

## Core Model

**PMContext is the sole Entity (source). PRD and Sketch are its downstream Views.**

## Activation

When the user invokes this local Skill, run `/pm-setup` to configure the project.

After setup, use the command Skills:

- `/pm-need` — collect materials + refine into PMContext
- `/pm-prd` — generate PRD from PMContext
- `/pm-sketch` — generate sketches from PMContext

The detailed workflow rules live in `CONTEXT.md` and each Skill's `SKILL.md`.

## Installer Note

```bash
npx skills@latest add Wcof/PMSkill --all
```
