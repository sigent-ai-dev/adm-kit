# Implementation Plan: Implement `adm init`

**Branch**: `feature/4-adm-init` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

## Summary

Implement the `adm init <domain>` CLI command using typer + rich. Uses `importlib.resources` to access bundled templates. Creates state file, artefact directories, and installs command files to the target AI agent directory.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: typer, rich, pydantic v2, importlib.resources (stdlib)

**Storage**: Local filesystem (`.adm/project.json`, `artefacts/`, agent command dirs)

**Testing**: pytest with tmp_path fixtures

**Target Platform**: macOS, Linux, Windows (via uv tool install)

**Project Type**: CLI tool

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| II. Phase Gates Are Hard | PASS | Init sets phase to 1, no skipping |
| III. Preserve Analyst Work | PASS | Refuses re-init without --force |
| VI. Templates Over Code | PASS | Intelligence in templates, CLI is thin |

## Project Structure

```text
src/adm_cli/
├── __init__.py          # UPDATE — replace stub with real implementation
├── schema.py            # EXISTS — state schema (issue #1)
├── init.py              # NEW — init command implementation
└── templates/           # NEW — bundled templates (package data)
    ├── __init__.py
    ├── commands/        # Copied from templates/commands/
    │   ├── lineage.md
    │   ├── inventory.md
    │   ├── invariants.md
    │   ├── thesis.md
    │   ├── validate.md
    │   ├── ratchet.md
    │   ├── model.md
    │   └── clarify.md
    └── phases/          # Copied from templates/phases/
        ├── 1-lineage.md
        ├── 2-inventory.md
        └── ...

tests/
├── test_cli.py          # EXISTS — smoke test
└── test_init.py         # NEW — init command tests
```

## Key Design Decisions

1. **Templates bundled as package data**: `src/adm_cli/templates/` is included in the wheel via hatch build config. Accessed at runtime via `importlib.resources`.

2. **Agent directory mapping**:
   ```python
   AGENT_DIRS = {
       "claude": ".claude/commands",
       "gemini": ".gemini/commands",
       "copilot": ".github/agents",
       "cursor": ".cursor/commands",
       "q": ".amazonq/prompts",
       "windsurf": ".windsurf/workflows",
   }
   ```

3. **Command file naming**: Commands are installed with `adm.` prefix (e.g., `adm.lineage.md`) so they appear as `/adm.lineage` in agents.

4. **State file creation**: Uses `schema.py`'s `load_state()` / `save_state()` for atomic read-modify-write.

5. **Source path**: Stored in domain state as `source_path` (new optional field to add to schema).
