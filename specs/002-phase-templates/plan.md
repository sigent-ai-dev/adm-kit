# Implementation Plan: Phase Artefact Templates

**Branch**: `feature/2-phase-templates` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-phase-templates/spec.md`

## Summary

Create 7 markdown template files (one per ADM phase) in `templates/phases/` with YAML frontmatter declaring expected output files. Each template documents inputs, outputs, artefact structure, and completion criteria for its phase.

## Technical Context

**Language/Version**: Markdown with YAML frontmatter (no code required)

**Primary Dependencies**: None — pure template files

**Storage**: Files in `templates/phases/`

**Testing**: Manual review + future `adm check` integration

**Target Platform**: Any OS (markdown files)

**Project Type**: Template pack (part of CLI toolkit)

**Performance Goals**: N/A

**Constraints**: Templates must be parseable by Python's `yaml` stdlib module for frontmatter extraction

**Scale/Scope**: 7 template files, each ~50-100 lines

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Discover, Don't Prescribe | PASS | Templates define structure, not content |
| II. Phase Gates Are Hard | PASS | Templates enable gate validation via expected_outputs |
| III. Preserve Analyst Work | PASS | Templates don't touch resolutions |
| IV. Falsify Before Ratcheting | PASS | Thesis template documents versioning |
| V. Immutable Contracts | PASS | Ratchet template documents semver |
| VI. Templates Over Code | PASS | This IS the template work |

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-templates/
├── spec.md
├── plan.md              # This file
├── tasks.md
├── research.md
├── data-model.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
templates/phases/
├── 1-lineage.md
├── 2-inventory.md
├── 3-invariants.md
├── 4-thesis.md
├── 5-validate.md
├── 6-ratchet.md
└── 7-model.md
```

**Structure Decision**: One template file per phase, numbered to match the artefact directory convention. Stored in `templates/phases/` alongside existing `templates/commands/`.

## Template Format

Each template file uses this structure:

```yaml
---
phase: <number>
name: <phase-name>
expected_outputs:
  - filename: <file>
    format: md|json|py
    required: true|false
  - filename: <file>
    format: md|json|py
    required: true|false
versioned: true|false
depends_on:
  phase: <prior-phase-number>
  artefacts:
    - <filename>
---
```

Followed by markdown body with sections:
- **Purpose** — what this phase achieves
- **Inputs** — what's needed from prior phases
- **Process** — what the analyst/agent does
- **Outputs** — detailed description of each expected artefact
- **Completion Criteria** — what "done" looks like for gate advancement

## Phase-Specific Design

| Phase | Expected Outputs | Versioned |
|-------|-----------------|-----------|
| 1-lineage | `lineage.md`, `lineage.json` | No |
| 2-inventory | `inventory.md`, `inventory.json` | No |
| 3-invariants | `invariants.md`, `invariants.py`, `invariants.json` | No |
| 4-thesis | `thesis.md`, `draft.py`, `draft.schema.json` | Yes (v1/, v2/) |
| 5-validate | `report.md`, `report.json` | Yes (v1/, v2/) |
| 6-ratchet | `contract.py`, `contract.schema.json` | No (semver dirs: v1.0.0/) |
| 7-model | `feature.json`, `spec.md` | No |

## Complexity Tracking

No constitution violations. No complexity justification needed.
