---
phase: 5
name: validate
expected_outputs:
  - filename: report.md
    format: md
    required: true
  - filename: report.json
    format: json
    required: true
versioned: true
versioning: iteration
depends_on:
  phase: 4
  artefacts:
    - thesis.md
    - draft.py
    - draft.schema.json
---

# Phase 5: Validate

## Purpose

Attempt to falsify the thesis by running the proposed Pydantic model against real data snapshots. Validation is adversarial — the goal is to find records that break the model. Only an unfalsified thesis can be ratcheted to a contract.

## Inputs

- `draft.py` from Phase 4 (the Pydantic model to test)
- `draft.schema.json` from Phase 4 (for JSON-based validation)
- Source data file(s) — real snapshots, not synthetic test data
- `invariants.py` from Phase 3 (run alongside for regression)

## Process

1. **Load the model** — import the Pydantic model from `draft.py`
2. **Load real data** — read source files into records
3. **Validate each record** — attempt to construct a model instance from each row
4. **Collect failures** — capture ValidationError details (field, value, error type)
5. **Run invariants** — execute `invariants.py` suite as a regression check
6. **Classify results** — determine if failures are model bugs, data bugs, or edge cases
7. **Produce report** — summarise pass/fail with actionable findings
8. **Version the output** — place in `v<N>/` matching the thesis version being validated

## Outputs

All outputs live in a versioned subdirectory: `artefacts/<domain>/5-validation/v<N>/`

### `report.md`

Human-readable validation report:

```markdown
# Validation Report: <domain> v<N>

## Summary

- **Total records**: 10,000
- **Passed**: 9,847 (98.5%)
- **Failed**: 153 (1.5%)
- **Verdict**: FAIL — thesis requires iteration

## Failure Analysis

| # | Field | Error Type | Count | Example Value | Recommendation |
|---|-------|-----------|-------|---------------|----------------|
| 1 | balance | less_than | 23 | -0.01 | Relax ge=0 constraint or add nullable |
| 2 | account_id | pattern | 130 | ACC-12345 | Extend pattern to 5 digits |

## Invariant Regression

- INV-001: PASS
- INV-002: FAIL (23 records) — related to balance constraint above

## Recommendations

- [ ] Update thesis to handle 5-digit account IDs
- [ ] Investigate negative balances — are they valid or data quality issues?
```

### `report.json`

Machine-readable validation results:

```json
{
  "domain": "<domain-name>",
  "thesis_version": 1,
  "total_records": 10000,
  "passed": 9847,
  "failed": 153,
  "verdict": "fail",
  "failures": [
    {
      "field": "balance",
      "error_type": "less_than",
      "count": 23,
      "example_value": -0.01
    }
  ]
}
```

## Completion Criteria

- Validation ran against real data (not synthetic/mocked)
- Every record in the source was tested (no sampling unless documented)
- Failures are classified with actionable recommendations
- Invariant regression suite was executed
- Verdict is clearly stated: PASS (can ratchet) or FAIL (needs thesis iteration)
- If FAIL: specific recommendations for thesis v(N+1) are provided
- Report version matches the thesis version being validated
