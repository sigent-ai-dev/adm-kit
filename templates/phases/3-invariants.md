---
phase: 3
name: invariants
expected_outputs:
  - filename: invariants.md
    format: md
    required: true
  - filename: invariants.py
    format: py
    required: true
  - filename: invariants.json
    format: json
    required: true
versioned: false
depends_on:
  phase: 2
  artefacts:
    - inventory.md
    - inventory.json
---

# Phase 3: Invariants

## Purpose

Extract cross-cutting rules that the data must satisfy. Invariants are constraints that hold across all valid records — they are the "laws" of the data domain. Each invariant is expressed in three forms: human-readable, executable (pytest), and machine-readable (JSON).

## Inputs

- `inventory.md` / `inventory.json` from Phase 2
- `lineage.md` from Phase 1 (business context for why rules exist)
- Source data file(s) (to verify invariants against actual records)

## Process

1. **Identify candidate invariants** — from column types, relationships, business rules
2. **Classify each invariant** — uniqueness, referential, range, format, conditional, cross-field
3. **Assign identifiers** — each invariant gets an INV-NNN code
4. **Write pytest assertions** — each invariant as a runnable test function
5. **Verify against data** — run invariants against source to confirm they hold
6. **Mark status** — PASSING, FAILING (with explanation), or PENDING (needs analyst input)

## Outputs

### `invariants.md`

Human-readable invariant catalogue:

| ID | Type | Description | Status | Columns |
|----|------|-------------|--------|---------|
| INV-001 | uniqueness | account_id is unique across all records | PASSING | COL-001 |
| INV-002 | range | balance is always >= 0 | PASSING | COL-002 |
| INV-003 | format | account_id matches pattern ACC-\d{4} | PENDING | COL-001 |

### `invariants.py`

Executable pytest suite:

```python
import pytest
import pandas as pd

@pytest.fixture
def data():
    return pd.read_csv("source_data.csv")

def test_inv_001_account_id_unique(data):
    """INV-001: account_id is unique across all records."""
    assert data["account_id"].is_unique

def test_inv_002_balance_non_negative(data):
    """INV-002: balance is always >= 0."""
    assert (data["balance"] >= 0).all()
```

### `invariants.json`

Machine-readable invariant definitions:

```json
{
  "domain": "<domain-name>",
  "invariants": [
    {
      "id": "INV-001",
      "type": "uniqueness",
      "description": "account_id is unique across all records",
      "columns": ["COL-001"],
      "status": "passing"
    }
  ]
}
```

## Completion Criteria

- All obvious invariants are captured (no known rules left undocumented)
- Each invariant has an INV-NNN identifier
- Each invariant is expressed in all three forms (md, py, json)
- pytest suite runs without import errors (individual tests may FAIL — that's acceptable, it means the invariant is falsified)
- No invariant has status PENDING (all must be PASSING or FAILING with explanation)
- Zero PENDING invariants is required before Phase 6 (ratchet) can proceed
