---
phase: 4
name: thesis
expected_outputs:
  - filename: thesis.md
    format: md
    required: true
  - filename: draft.py
    format: py
    required: true
  - filename: draft.schema.json
    format: json
    required: true
versioned: true
versioning: iteration
depends_on:
  phase: 3
  artefacts:
    - invariants.md
    - invariants.py
    - invariants.json
---

# Phase 4: Thesis

## Purpose

Propose a candidate Pydantic model as a falsifiable claim about the data domain's structure. The thesis is NOT a final schema — it's a hypothesis: "this typed model correctly describes this data." Phase 5 will attempt to falsify it.

## Inputs

- `inventory.md` / `inventory.json` from Phase 2 (what columns exist)
- `invariants.md` / `invariants.py` from Phase 3 (what rules the data obeys)
- `lineage.md` from Phase 1 (business context)
- Source data file(s) (reference for type inference)

## Process

1. **Group columns into entities** — identify natural boundaries (one record type vs. multiple)
2. **Infer types** — from inventory types + invariants, choose Pydantic field types
3. **Apply constraints** — encode invariants as Pydantic validators where possible
4. **Write the model** — produce a complete Pydantic v2 BaseModel
5. **Generate JSON Schema** — derive from the Pydantic model (not hand-written)
6. **Document the thesis** — explain what the model claims and what would falsify it
7. **Version the output** — place in `v<N>/` subdirectory (v1 for first attempt)

## Outputs

All outputs live in a versioned subdirectory: `artefacts/<domain>/4-thesis/v<N>/`

### `thesis.md`

The claim being made:

- **Claim**: "This Pydantic model correctly describes all records in the <domain> dataset"
- **Key decisions**: Why certain types/constraints were chosen
- **Known risks**: Where the model might break (edge cases from invariants)
- **Falsification criteria**: What would prove this thesis wrong

### `draft.py`

Complete Pydantic v2 model:

```python
from pydantic import BaseModel, Field, field_validator

class HoldingsRecord(BaseModel):
    account_id: str = Field(..., pattern=r"^ACC-\d{4}$")
    balance: float = Field(..., ge=0)
    # ... all fields from inventory
```

### `draft.schema.json`

JSON Schema derived from the Pydantic model:

```python
# Generated via:
import json
print(json.dumps(HoldingsRecord.model_json_schema(), indent=2))
```

## Completion Criteria

- Pydantic model covers all columns from the inventory (no field omissions)
- Model compiles without errors (`python -c "from draft import *"`)
- JSON Schema is generated from the model (not hand-written)
- Thesis document clearly states what would falsify the claim
- Output is in a versioned subdirectory (`v1/` for first iteration)
- If this is a re-iteration (v2+), document what changed from the prior version
