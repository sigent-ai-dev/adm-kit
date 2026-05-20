# Implementation Plan: AI Agent Command Files

**Branch**: `feature/3-command-files` | **Date**: 2026-05-20 | **Spec**: [spec.md](./spec.md)

## Summary

Complete and standardise the 7 existing phase command files, create the new `/adm.clarify` utility command, and unify the clarification ID namespace to `CLR-NNN` across all commands. Each command file must include frontmatter, gate check, execution flow, output structure, and guidelines.

## Technical Context

**Language/Version**: Markdown with YAML frontmatter (no code)

**Primary Dependencies**: None — pure template files

**Storage**: Files in `templates/commands/`

**Testing**: Validate structure (frontmatter, required sections), cross-reference with phase templates

**Target Platform**: Any AI agent (agent-agnostic markdown)

**Project Type**: Template pack

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Discover, Don't Prescribe | PASS | Commands instruct discovery process |
| II. Phase Gates Are Hard | PASS | Gate checks enforce this |
| III. Preserve Analyst Work | PASS | Clarify command preserves resolutions |
| IV. Falsify Before Ratcheting | PASS | Validate command implements this |
| V. Immutable Contracts | PASS | Ratchet command enforces this |
| VI. Templates Over Code | PASS | This IS the template work |

## Project Structure

### Source Code (repository root)

```text
templates/commands/
├── lineage.md          # Phase 1 — UPDATE (OQ→CLR, review completeness)
├── inventory.md        # Phase 2 — UPDATE (review completeness)
├── invariants.md       # Phase 3 — UPDATE (review completeness)
├── thesis.md           # Phase 4 — UPDATE (review completeness)
├── validate.md         # Phase 5 — UPDATE (review completeness)
├── ratchet.md          # Phase 6 — UPDATE (review completeness)
├── model.md            # Phase 7 — UPDATE (review completeness)
└── clarify.md          # Utility — NEW
```

## Command File Standard Structure

Every command file must have:

```markdown
---
description: <one-line description including phase number>
handoffs:
  - label: <next action>
    agent: <next command>
    prompt: <what to do next>
    send: true
---

## User Input

\```text
$ARGUMENTS
\```

## Outline

<brief description of what this command does>

### Gate Check

<prerequisites that must be met before execution>

### Execution Flow

<numbered steps the agent follows>

### Output Structure

<expected output format/schema>

## Guidelines

<rules, anti-patterns, and tips>
```

## Changes Required

| File | Action | Changes |
|------|--------|---------|
| `lineage.md` | Update | Replace `OQ-NNN` with `CLR-NNN`; verify all sections present |
| `inventory.md` | Review | Verify completeness against standard |
| `invariants.md` | Review | Verify completeness against standard |
| `thesis.md` | Review | Ensure iteration versioning documented |
| `validate.md` | Review | Ensure iteration versioning documented |
| `ratchet.md` | Review | Ensure zero-PENDING gate is explicit |
| `model.md` | Review | Ensure Spec Kit handoff is clear |
| `clarify.md` | Create | New utility command for resolving CLR-NNN questions |

## `/adm.clarify` Design

The clarify command is unique: it can run at any phase and doesn't produce phase artefacts. Instead, it manages the resolution of `CLR-NNN` questions raised by other phases.

**Gate**: None (usable at any phase)
**Inputs**: `.adm/project.json` (resolutions), current phase artefacts (for context)
**Outputs**: Updated resolutions in state file, optionally updated artefacts
**Flow**: List open → select → resolve → update state → report remaining
