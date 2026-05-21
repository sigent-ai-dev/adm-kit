# Changelog

All notable changes to ADM Kit will be documented in this file.

## [Unreleased]

## [0.1.0] - 2026-05-21

### Added

- `adm init <domain>` — initialise a domain with artefact scaffolding and AI agent commands
- `adm check` — validate project state, artefact existence, CLR status, invariant suite
- `adm status` — Rich table showing per-domain phase progression
- Phase gate enforcement (`can_advance`, `advance_phase`) with template-driven validation
- Clarify-gate pattern — structured CLR-NNN questions with merge/overwrite/skip modes
- Auto-semver bumping from JSON Schema diff (major/minor/patch)
- Stability window enforcement for ratcheting
- Spec Kit integration — `/adm.model` seeds feature directories from contracts
- Multi-agent support — format adaptation for Claude, Gemini, Copilot, Cursor, Q, Windsurf
- 7 phase templates with YAML frontmatter (expected_outputs, depends_on)
- 8 command templates (7 phases + /adm.clarify utility)
- 115 tests (unit + integration)
- GitHub Actions CI (Python 3.11 + 3.12)
- GitHub Actions release workflow (tag → PyPI + GitHub Release)
