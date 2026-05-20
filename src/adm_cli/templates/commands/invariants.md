---
description: Extract cross-cutting rules that must hold regardless of schema iteration — Phase 3 of ADM.
handoffs:
  - label: Propose Thesis
    agent: adm.thesis
    prompt: Produce a candidate schema as a falsifiable claim
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.invariants` is Phase 3. It extracts rules that must hold true for ANY valid schema in this domain — regardless of how the thesis evolves through iterations.

### Gate Check

- Phase 2 (inventory) must be complete
- `artefacts/<domain>/2-inventory/inventory.json` must exist

### Execution Flow

1. **Load lineage + inventory**.

2. **Identify invariant categories**:
   - **Uniqueness**: Which columns/combinations must be unique?
   - **Nullability**: Which columns must never be null?
   - **Referential**: Which columns reference values in other columns/files?
   - **Range**: Which numeric columns have known bounds?
   - **Format**: Which string columns have format constraints (dates, codes, IDs)?
   - **Cardinality**: Which relationships are 1:1, 1:N, N:M?
   - **Business rules**: Which domain-specific rules exist? (from VBA, documentation, analyst knowledge)

3. **For each invariant**, produce three representations:

   **Markdown** (human-readable):
   ```markdown
   ### INV-NNN: <title>

   **Category**: uniqueness | nullability | referential | range | format | cardinality | business
   **Applies to**: COL-NNN [, COL-NNN, ...]
   **Rule**: [natural language statement of the rule]
   **Confidence**: [high | medium | low]
   **Source**: [where this rule was discovered — lineage, data inspection, analyst input]
   **Status**: [confirmed | pending]
   ```

   **Python** (executable pytest):
   ```python
   def test_inv_nnn_title(snapshot_df):
       """INV-NNN: <title>"""
       assert snapshot_df["column"].notna().all(), "column must never be null"
   ```

   **JSON** (machine-readable manifest):
   ```json
   {
     "id": "INV-NNN",
     "title": "...",
     "category": "nullability",
     "columns": ["COL-001"],
     "rule": "...",
     "confidence": "high",
     "status": "confirmed"
   }
   ```

4. **Handle uncertain invariants**:
   - If a rule MIGHT hold but you can't confirm from data alone: mark `status: "pending"`
   - Pending invariants are legitimate — they mean "the rule exists but the assertion isn't codified yet"
   - Pending invariants DO NOT block Phase 4 (thesis) but DO block Phase 6 (ratchet)

5. **Write artefacts** to `artefacts/<domain>/3-invariants/`:
   - `invariants.md` — narrative with all rules
   - `invariants.py` — pytest module (runnable)
   - `invariants.json` — manifest

6. **Update state** and **write audit entry**.

## Guidelines

- Invariants are the safety net. They catch schema regressions across thesis iterations.
- Prefer more invariants over fewer. False positives are cheap to fix; missed rules become production bugs.
- Business rules from VBA/formulas are the highest-value invariants — they encode domain knowledge that would otherwise be lost.
- Pending invariants are fine at Phase 3. They become blockers only at Phase 6 (ratchet).
