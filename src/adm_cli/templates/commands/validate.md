---
description: Run thesis validation against real snapshots — Phase 5 of ADM.
handoffs:
  - label: Ratchet Contract
    agent: adm.ratchet
    prompt: Promote this stable thesis to an immutable contract
    send: true
  - label: Revise Thesis
    agent: adm.thesis
    prompt: Produce a new thesis version addressing validation failures
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.validate` is Phase 5. It attempts to FALSIFY the thesis by running it against real data snapshots. The output is a pass/fail report.

### Gate Check

- Phase 4 (thesis) must have at least one version
- `artefacts/<domain>/4-thesis/v{N}/draft.py` must exist
- Real snapshot data must be accessible

### Execution Flow

1. **Load the thesis** (latest version or user-specified version).

2. **Load real snapshots** — actual production data, not synthetic fixtures.

3. **Run validation**:

   a. **Schema validation**: Attempt to parse every row through the Pydantic model.
      - Record: rows passed, rows failed, failure reasons per row
      - Group failures by field and error type

   b. **Invariant validation**: Run the Phase 3 pytest suite against the snapshot.
      - Record: invariants passed, failed, pending (not yet codified)

   c. **Coverage check**: Are there columns in the snapshot not covered by the thesis?

4. **Produce stability assessment**:
   - **PASS**: All rows parse, all confirmed invariants pass
   - **FAIL**: Rows fail parsing OR confirmed invariants fail
   - **PENDING**: Passes confirmed invariants but pending invariants exist

5. **Write report** to `artefacts/<domain>/5-validation/v{N}/`:
   ```markdown
   # Validation Report — <domain> thesis v{N}

   **Snapshot**: [source file/date]
   **Rows tested**: [N]
   **Outcome**: PASS | FAIL | PENDING

   ## Schema Validation
   - Rows passed: [N] ([%])
   - Rows failed: [N] ([%])
   - Failure breakdown: [by field, by error type]

   ## Invariant Validation
   - Confirmed passed: [N/M]
   - Confirmed failed: [N/M] — [list]
   - Pending (not runnable): [N]

   ## Ratchet Readiness
   - [x] All rows parse successfully
   - [x] All confirmed invariants pass
   - [ ] No pending invariants remain (required for ratchet)
   - [ ] Stability window elapsed (if configured)
   ```

6. **Update state** and **write audit entry**.

7. **Recommend next step**:
   - If PASS + no pending → ready for `/adm.ratchet`
   - If PASS + pending → resolve pending invariants first
   - If FAIL → list failures, recommend `/adm.thesis` revision

## Guidelines

- ALWAYS use real data. Synthetic fixtures don't catch real-world edge cases.
- A FAIL is not a problem — it's the methodology working. The thesis was wrong; now we know how.
- Report failures specifically enough that the next thesis iteration can address each one.
- Don't fix the thesis here — that's Phase 4's job. This phase only reports.
