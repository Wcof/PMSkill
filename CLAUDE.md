# PMSkill

Skills are organized into bucket folders under `skills/`:

- `setup/` — 初始化配置
- `discovery/` — 需求发现（collect + refine → PMContext）
- `delivery/` — 交付（PRD 生成）
- `visualization/` — 可视化（草图生成）

Every skill must have a reference in the top-level `README.md`. Each bucket folder has a `README.md` that lists every skill with a one-line description, grouped into **User-invoked** and **Model-invoked**.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true`, reachable only by the human) or model-invoked (model- or user-reachable). A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

## Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at repo root.
