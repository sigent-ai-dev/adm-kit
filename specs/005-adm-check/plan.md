# Implementation Plan: ADM Check — State Validation

**Branch**: `feature/5-adm-check` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-adm-check/spec.md`

## Summary

Implement `adm check` command that validates project state: schema integrity, artefact directory existence, open clarification count, and optional invariant suite execution. Uses subprocess pytest for invariant runs. Produces rich-formatted output with severity-coloured findings.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: typer, rich, pydantic v2, subprocess (stdlib for pytest invocation)

**Storage**: Reads `.adm/project.json` (filesystem)

**Testing**: pytest with tmp_path fixtures

**Target Platform**: macOS, Linux, Windows

**Project Type**: CLI tool

**Performance Goals**: <5s for up to 10 domains (excluding invariant test runtime)

**Constraints**: Invariant suite runs as subprocess (`python -m pytest`) to isolate from the check command's own process

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| II. Phase Gates Are Hard | PASS | Check validates that artefact dirs exist for claimed phases |
| III. Preserve Analyst Work | PASS | Check reports CLR status but never modifies resolutions |
| VI. Templates Over Code | PASS | Check is thin state management — no domain intelligence |

Post-design re-check: PASS (no violations introduced).

## Project Structure

### Documentation (this feature)

```text
specs/005-adm-check/
├── spec.md
├── plan.md              # This file
├── data-model.md
├── tasks.md             # /speckit-tasks output
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
src/adm_cli/
├── __init__.py          # UPDATE — wire check command
├── check.py             # NEW — check command implementation
└── schema.py            # EXISTS — load_state()

tests/
├── test_check.py        # NEW — check command tests
├── test_init.py         # EXISTS
└── test_schema.py       # EXISTS
```

**Structure Decision**: Single module `check.py` with a `run_check()` function, following the same pattern as `init.py`.

## Research

### Decision: Invariant suite execution method

**Decision**: Run invariants via `subprocess.run(["python", "-m", "pytest", path, "--tb=short", "-q"])` capturing stdout/stderr.

**Rationale**: Process isolation prevents invariant import errors from crashing `adm check`. Subprocess also lets us capture exit code (0=pass, non-zero=failures) cleanly.

**Alternatives considered**:
- Import and run pytest programmatically (`pytest.main()`) — rejected because invariants may import domain-specific packages that aren't in the CLI's environment
- Parse invariants.py as AST — rejected because it can't actually execute the tests

### Decision: Severity model

**Decision**: Three severities — `error` (blocks, causes non-zero exit), `warning` (informs, doesn't block), `info` (contextual).

**Rationale**: Maps to the spec's distinction: structural issues (missing dirs, invalid schema) are errors; open CLRs and invariant failures are warnings; phase status is info.

## Data Model

### CheckFinding

| Field | Type | Description |
|-------|------|-------------|
| severity | error / warning / info | Determines exit code impact |
| domain | str | Which domain this applies to |
| message | str | Human-readable description |
| phase | int? | Which phase (if phase-specific) |

### CheckReport

| Field | Type | Description |
|-------|------|-------------|
| findings | list[CheckFinding] | All findings across all domains |
| errors | int | Count of error-severity findings |
| warnings | int | Count of warning-severity findings |
| passed | bool | True if errors == 0 |

## Contracts

### CLI Interface

```
adm check [--domain <name>]
```

- No arguments: check all domains
- `--domain`: check a specific domain only
- Exit 0: all checks pass (warnings OK)
- Exit 1: errors found

### Output Format

```
ADM Check: <project-dir>

  holdings (phase 3):
    ✓ State file valid
    ✓ artefacts/holdings/1-lineage/ exists
    ✓ artefacts/holdings/2-inventory/ exists
    ✓ artefacts/holdings/3-invariants/ exists
    ⚠ 2 open clarifications (CLR-001, CLR-003)
    ⚠ Invariants: 5 passed, 1 failed

Summary: 0 errors, 2 warnings — PASS
```
