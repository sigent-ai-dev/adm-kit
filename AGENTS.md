# AGENTS.md

## About ADM Kit

**ADM Kit** is a toolkit for implementing Analysis-Driven Modelling — a seven-phase methodology for discovering, validating, and versioning data schemas from messy real-world sources. It handles the class of work where data shapes are discovered, not specified.

**ADM CLI** is the command-line interface that bootstraps projects with the ADM framework, manages per-domain state, and enforces phase gates.

## Development Context

This project uses Spec Kit's methodology to develop itself. Use `/speckit.specify` to specify features, `/speckit.plan` to plan them, and `/speckit.implement` to build them. Use Intent Kit's `/intent.capture` to frame the big-picture intent for ADM Kit itself.

## Architecture

### CLI (`src/adm_cli/`)

Python package using `typer` + `rich`, distributed via `uv tool install`:

- `adm init <domain> --source <path>` — initialise a domain with source data
- `adm check` — validate state, gates, invariants
- `adm status` — show per-domain phase progression

### Templates (`templates/`)

- **`commands/*.md`** — AI agent command files (one per phase)
- **`phases/*.md`** — Phase-specific artefact templates
- **`state-schema.py`** — Pydantic schema for `.adm/project.json`

### Commands (`templates/commands/`)

Seven phase commands plus utilities:

| Command | Phase | Input | Output |
|---------|-------|-------|--------|
| `/adm.lineage` | 1 | Source data + domain knowledge | `lineage.{md,json}` |
| `/adm.inventory` | 2 | lineage + source files | `inventory.{md,json}` |
| `/adm.invariants` | 3 | lineage + inventory | `invariants.{md,py,json}` |
| `/adm.thesis` | 4 | invariants + inventory | `thesis.md` + `draft.py` + `draft.schema.json` |
| `/adm.validate` | 5 | thesis + real snapshots | `report.{md,json}` |
| `/adm.ratchet` | 6 | stable thesis | `contract.py` + `contract.schema.json` |
| `/adm.model` | 7 | ratcheted contract | Spec Kit feature directory |
| `/adm.clarify` | any | Open questions | Resolved analyst decisions |

### State (`.adm/project.json`)

```json
{
  "domains": {
    "holdings": {
      "current_phase": 4,
      "iteration": 2,
      "contract_version": null,
      "resolutions": {
        "CLR-001": "resolved",
        "CLR-002": "open"
      }
    }
  }
}
```

### Artefact Layout

Per ADR 0027 (phase-numbered artefact layout):

```
artefacts/<domain>/<N>-<phase>/
```

Each phase writes to its numbered directory. Thesis and validation support versioned subdirectories (`v1/`, `v2/`, ...) for iteration.

## Implementation Plan

### Phase A: Foundation (current)

- [x] Project structure mirroring Spec Kit / Intent Kit
- [x] README with full workflow documentation
- [x] AGENTS.md with development context
- [ ] Template files for all 7 phases
- [ ] Command files for all AI agents
- [ ] State schema (Pydantic)
- [ ] Constitution / memory file
- [ ] pyproject.toml with CLI entry point

### Phase B: CLI Implementation

- [ ] `adm init <domain>` — create domain directory + state entry
- [ ] `adm check` — validate per-domain state, run invariant suite
- [ ] `adm status` — display domain progression table
- [ ] Phase gate enforcement in state manager
- [ ] Clarify-gate pattern: raise structured questions, preserve resolutions across re-runs

### Phase C: Phase Commands

- [ ] `/adm.lineage` — trace data lifecycle, touchpoints, mutations
- [ ] `/adm.inventory` — catalogue every column (COL-NNN namespace)
- [ ] `/adm.invariants` — extract rules as Markdown + pytest + JSON
- [ ] `/adm.thesis` — produce candidate Pydantic model as falsifiable claim
- [ ] `/adm.validate` — run thesis against snapshots, produce pass/fail report
- [ ] `/adm.ratchet` — promote stable thesis to semver contract
- [ ] `/adm.model` — hand off to Spec Kit by seeding feature directory

### Phase D: Advanced Features

- [ ] Wide-file handling (>1000 columns → chunk strategy)
- [ ] Analyst resolution preservation across re-runs
- [ ] Stability window enforcement for ratcheting
- [ ] Auto-semver bumping from schema diff
- [ ] Multi-domain state management

### Phase E: Agent Integration

- [ ] Claude Code commands
- [ ] Gemini CLI commands
- [ ] GitHub Copilot agents
- [ ] Cursor commands
- [ ] Amazon Q Developer prompts
- [ ] Windsurf workflows

### Phase F: Spec Kit Integration

- [ ] `/adm.model` seeds `specs/NNN-<domain>-engine/` directory
- [ ] Produces `feature.json` + `spec.md` consumable by Spec Kit
- [ ] Traceability from contract fields to feature requirements

### Phase G: Testing & Release

- [ ] Unit tests for state management
- [ ] Integration tests (full 7-phase flow with sample data)
- [ ] GitHub Actions CI
- [ ] Release workflow
- [ ] Documentation site

## Key Design Decisions

1. **Phase-numbered directories** — artefacts live at `artefacts/<domain>/<N>-<phase>/` so you can see at a glance what exists and what phase produced it.
2. **Pydantic as the contract format** — typed Python models are both human-readable and machine-executable. JSON Schema is derived, not hand-written.
3. **Clarify gate preserves analyst work** — resolutions survive re-runs. The `--resolutions` flag controls merge behaviour.
4. **Thesis is a falsifiable claim** — "this model describes this data" is a hypothesis. Validation attempts to falsify it. Only unfalsified theses get ratcheted.
5. **Ratcheted contracts are immutable** — changes require a new semver version. No editing in place.
6. **Templates over code** — the intelligence lives in command markdown (consumed by AI), not in Python. The CLI is thin state management.

## Portability

ADM is engagement-portable. The seven phases, state schema, artefact layout, and clarify-gate pattern transfer to any domain where messy real-world data needs to be modelled:
- Financial data migration
- Legacy database modernisation
- Spreadsheet-to-API conversion
- Data warehouse schema discovery
- Regulatory reporting standardisation
