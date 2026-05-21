# Development Workflow

## Spec-Driven Development

All features follow the Spec Kit workflow:
1. `/speckit-specify` — define the what and why
2. `/speckit-clarify` — de-risk ambiguities (skip for trivial features)
3. `/speckit-plan` — technical plan + data model
4. `/speckit-tasks` — actionable task breakdown
5. `/speckit-analyze` — cross-artifact consistency check
6. `/speckit-implement` — execute tasks

## Branch Convention

- Branch: `feature/<issue-number>-<short-name>`
- Spec directory: `specs/<NNN>-<short-name>/`
- One issue per branch, one PR per issue

## Commit Messages

- Imperative mood, present tense
- First line: what changed (under 72 chars)
- Body: why + what it enables
- Footer: `Closes #N` when all AC are met

## PR Checklist

Before creating a PR:
- All tests pass (`uv run --group dev pytest`)
- No unused imports or dead code
- Spec followed (reference in PR body)
- Self-review completed (no stubs, no tautological tests)

## CI Requirements

- Tests must pass on Python 3.11 and 3.12
- Branch protection: CI must pass before merge
- Squash merge to main

## Documentation Sync

After completing a feature:
- Update AGENTS.md if architecture or commands changed
- Update README.md if user-facing capabilities changed
- Keep `.specify/feature.json` pointing to current work
