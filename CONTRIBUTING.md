# Contributing

Thanks for contributing to PRD Helper.

## Development Setup

1. Fork and clone the repository.
2. Install required tools (`python3` recommended).
3. Run checks locally before opening a PR:

```bash
python3 -m py_compile scripts/*.py scripts/lib/*.py modules/*/scripts/*.py
python3 -m pytest tests
```

## Pull Request Rules

- Keep PRs focused and small.
- Use clear commit messages.
- Update docs when behavior/commands/templates change.
- Include verification steps in PR description.

## Code Style

- Prefer existing patterns in this repository.
- Keep scripts deterministic and idempotent where possible.
- Do not commit temporary files or machine-specific outputs.
