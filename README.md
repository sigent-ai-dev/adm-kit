# ADM Kit

**Discover and model messy real-world data sources into versioned, typed contracts.**

ADM Kit is an open-source toolkit for Analysis-Driven Modelling (ADM) — a seven-phase methodology for migrating legacy data sources into structured, validated, versioned schemas. It is designed for the class of work where the data's shape is a reality to be **discovered**, not a requirement to be **written**.

ADM sits between [Intent Kit](https://github.com/superhighway-factory/intent-kit) (upstream — captures why the modelling is needed) and [Spec Kit](https://github.com/github/spec-kit) (downstream — implements features from the ratcheted contracts).

---

## What is Analysis-Driven Modelling?

Traditional spec-driven development assumes you know what you want to build. But when modernising legacy systems — spreadsheets, undocumented databases, tribal-knowledge processes — the schema is not a requirement to specify. It's a reality to discover, trace, validate, and pin.

ADM provides seven sequential phases:

```
lineage → inventory → invariants → thesis → validate → ratchet → model
```

Each phase produces versioned, immutable artefacts. The output is a typed contract (Pydantic model + JSON Schema) that downstream feature work can depend on.

## Why ADM Kit?

Without ADM:
- Teams write schemas by guessing, then discover edge cases in production
- Legacy business rules live in VBA/SQL/tribal knowledge with no structured capture
- Schema work gets forced through feature-story templates, losing analytical rigour
- Modernisation projects ship "v1" schemas that break on real data within weeks

With ADM:
- Every column of every file is catalogued (Phase 2)
- Cross-cutting invariants are codified as runnable tests (Phase 3)
- Schemas are proposed as falsifiable claims and validated against real data (Phases 4-5)
- Only stable, validated schemas get promoted to immutable contracts (Phase 6)
- Contracts hand off to Spec Kit for implementation (Phase 7)

## The Seven Phases

| # | Phase | Command | Output |
|---|-------|---------|--------|
| 1 | Lineage | `/adm.lineage` | Data lifecycle, touchpoints, mutations, open questions |
| 2 | Inventory | `/adm.inventory` | Catalogue of every column of every file |
| 3 | Invariants | `/adm.invariants` | Cross-cutting rules (Markdown + pytest + JSON) |
| 4 | Thesis | `/adm.thesis` | Candidate schema as a falsifiable claim |
| 5 | Validate | `/adm.validate` | Pass/fail report against real snapshots |
| 6 | Ratchet | `/adm.ratchet` | Promote to immutable, semver-versioned contract |
| 7 | Model | `/adm.model` | Hand-off to Spec Kit (seeds feature directory) |

Each phase is **gated** (next refuses to run until current completes), **versioned** (thesis/validation support multiple iterations), and **analyst-interactive** (surfaces clarification prompts where data semantics are unclear).

## Get Started

### 1. Install ADM CLI

```bash
uv tool install adm-cli --from git+https://github.com/superhighway-factory/adm-kit.git
```

### 2. Initialise a domain

```bash
adm init holdings --source ./data/holdings_snapshot.csv
```

### 3. Run lineage

```bash
/adm.lineage
```

### 4. Progress through phases

Each phase builds on the previous. The CLI enforces phase gates and tracks state in `.adm/project.json`.

## Supported AI Agents

| Agent | Directory | Status |
|-------|-----------|--------|
| Claude Code | `.claude/commands/` | Full |
| Gemini CLI | `.gemini/commands/` | Full |
| GitHub Copilot | `.github/agents/` | Full |
| Cursor | `.cursor/commands/` | Full |
| Amazon Q Developer | `.amazonq/prompts/` | Full |
| Windsurf | `.windsurf/workflows/` | Full |

## Project Structure (bootstrapped)

```
your-project/
├── .adm/
│   ├── project.json              # Per-domain phase state
│   └── schema.py                 # State file Pydantic schema
├── artefacts/
│   └── <domain>/
│       ├── 1-lineage/
│       │   └── lineage.{md,json}
│       ├── 2-inventory/
│       │   └── inventory.{md,json}
│       ├── 3-invariants/
│       │   └── invariants.{md,py,json}
│       ├── 4-thesis/
│       │   └── v1/
│       │       ├── thesis.md
│       │       ├── draft.py      # Pydantic model
│       │       └── draft.schema.json
│       ├── 5-validation/
│       │   └── v1/
│       │       └── report.{md,json}
│       ├── 6-contracts/
│       │   └── v1.0.0/           # Semver-versioned
│       │       ├── contract.py
│       │       └── contract.schema.json
│       └── 7-model/
│           └── feature.json      # Spec Kit handoff
├── memory/
│   └── constitution.md
└── specs/                         # Spec Kit feature dirs land here
```

## Core Concepts

### Discover and Falsify (not Specify and Satisfy)

ADM's shape is fundamentally different from feature development. The data's schema is not a requirement — it's a hypothesis that must be tested against real snapshots. A thesis (Phase 4) is a claim: "this Pydantic model correctly describes this data domain." Validation (Phase 5) attempts to falsify that claim.

### The Clarify Gate

When data semantics are unclear from the source alone — a column name is ambiguous, a formula references undocumented VBA, a sentinel value has no documentation — ADM raises a structured clarification question. The analyst resolves it, and the resolution is preserved across re-runs (so re-running Phase 1 doesn't destroy analyst work).

### Ratcheting

A contract is only promoted to `6-contracts/` when:
- Every invariant passes (no PENDING stubs)
- Validation runs against real snapshots without failure
- The stability window has elapsed (configurable, default: 0 — immediate for v1)
- The analyst explicitly confirms

Once ratcheted, a contract is immutable. Changes require a new semver version.

### Multi-domain Support

ADM operates per-domain. A single project can have multiple domains (e.g., `holdings`, `cashflows`, `derivatives`), each progressing through the seven phases independently. The state file tracks per-domain phase pointers.

## Integration

```
Intent Kit                     ADM Kit                        Spec Kit
─────────                     ───────                        ────────
/intent.capture               
/intent.decompose ──────▶     /adm.lineage (per domain)      
                              /adm.inventory                  
                              /adm.invariants                 
                              /adm.thesis                     
                              /adm.validate                   
                              /adm.ratchet                    
                              /adm.model ──────────────────▶  /speckit.specify
```

## Documentation

- [ADM Methodology](./adm-methodology.md)
- [Installation Guide](./docs/installation.md)
- [Quick Start](./docs/quickstart.md)
- [Phase Reference](./docs/phases.md)
- [Clarify Gate Pattern](./docs/clarify-gate.md)
- [Integration with Spec Kit](./docs/speckit-integration.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
