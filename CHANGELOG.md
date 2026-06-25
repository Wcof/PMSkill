# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- **Major restructure**: PMSkill refactored from PRD Context Compiler (4-stage pipeline) to Product Manager's Skill toolkit.
- PMContext is now the sole Entity; PRD and Sketch are downstream Views.
- 11 `prd-*` commands replaced by 12 `pm-*` Skills organized into 4 buckets (setup/discovery/delivery/visualization).
- Soft Gate / independent check mechanism replaced by explicit inline markers (`[待确认]`/`[假设]`/`[冲突]`).
- Relate phase dispersed into all Skills as built-in association discipline.
- Single-level traceability (sourced/unsourced) replaces Strong/Weak Trace two-level.
- No hooks — `/pm-collect` collects from conversation context directly.
- All Python runtime scripts, tests, and check infrastructure removed (pure Skill documentation-driven).

### Added

- Added GitHub governance files: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`.
- Added GitHub templates and CI workflow under `.github/`.
- Added `docs/github-project-kit.md` for project-cover prompt guidance and repository-structure standards.
