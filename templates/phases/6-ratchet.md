---
phase: 6
name: ratchet
expected_outputs:
  - filename: contract.py
    format: py
    required: true
  - filename: contract.schema.json
    format: json
    required: true
versioned: true
versioning: semver
depends_on:
  phase: 5
  artefacts:
    - report.md
    - report.json
---

# Phase 6: Ratchet

## Purpose

Promote a stable, validated thesis to an immutable, semver-versioned contract. Once ratcheted, a contract version is frozen — changes require a new version. This is the point of no return: the schema becomes a dependency that downstream systems can rely on.

## Inputs

- `draft.py` from Phase 4 (the validated Pydantic model)
- `report.md` / `report.json` from Phase 5 (proof of validation)
- `invariants.py` from Phase 3 (must all PASS — zero PENDING)
- Prior contract version (if exists) for semver diff

## Process

1. **Gate check** — refuse to ratchet if:
   - Validation verdict is FAIL
   - Any invariant is PENDING
   - Stability window has not elapsed (if configured)
2. **Determine version** — if first contract: `v1.0.0`. Otherwise:
   - Compare against prior version's JSON Schema
   - Breaking changes (removed fields, type narrowing) → MAJOR bump
   - Additive changes (new optional fields) → MINOR bump
   - No schema change (metadata only) → PATCH bump
3. **Freeze the contract** — copy `draft.py` → `contract.py` with version metadata
4. **Generate final schema** — derive `contract.schema.json` from the frozen model
5. **Record the ratchet** — update state with `contract_version`
6. **Create version directory** — place outputs in `v<MAJOR>.<MINOR>.<PATCH>/`

## Outputs

All outputs live in a semver directory: `artefacts/<domain>/6-contracts/v<X.Y.Z>/`

### `contract.py`

The frozen Pydantic model with version metadata:

```python
"""Contract: <domain> v1.0.0

Ratcheted: 2026-05-20
Thesis version: v3
Validation: PASS (10,000 records, 100%)
"""
from pydantic import BaseModel, Field

CONTRACT_VERSION = "1.0.0"

class HoldingsRecord(BaseModel):
    account_id: str = Field(..., pattern=r"^ACC-\d{4,5}$")
    balance: float = Field(..., ge=0)
    # ... frozen fields
```

### `contract.schema.json`

JSON Schema derived from the frozen contract model. This is the machine-readable interface that downstream systems consume.

## Completion Criteria

- Validation report shows PASS verdict
- Zero PENDING invariants (all PASSING or FAILING-with-explanation)
- Stability window elapsed (if configured; default 0 = immediate)
- Analyst explicitly confirms ratchet (not automatic)
- Contract version follows semver correctly relative to prior versions
- `contract.py` compiles without errors
- `contract.schema.json` is derived from `contract.py` (not hand-edited)
- Contract is placed in the correct semver directory
- State file updated with `contract_version`
- Once ratcheted, this version is IMMUTABLE — no edits, only new versions
