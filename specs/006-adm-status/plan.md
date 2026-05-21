# Implementation Plan: ADM Status — Progression Display

**Branch**: `feature/6-adm-status` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

## Summary

Implement `adm status` — a simple read-only command that loads `.adm/project.json` and renders a Rich table with per-domain phase progression. Follows the same pattern as check.py (load state, display, exit).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: typer, rich (Table), pydantic v2

**Project Type**: CLI tool — single function, ~40 lines

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| VI. Templates Over Code | PASS | Status is thin display logic |

## Project Structure

```text
src/adm_cli/
├── __init__.py          # UPDATE — wire status command
├── status.py            # NEW — status display implementation
└── schema.py            # EXISTS — load_state()

tests/
└── test_status.py       # NEW — status tests
```
