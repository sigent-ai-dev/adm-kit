---
description: Promote a stable thesis to an immutable, semver-versioned contract — Phase 6 of ADM.
handoffs:
  - label: Hand off to Spec Kit
    agent: adm.model
    prompt: Seed a Spec Kit feature directory from this contract
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.ratchet` is Phase 6. It promotes a validated thesis to an immutable contract. Once ratcheted, the contract cannot be modified — only a new semver version can supersede it.

### Gate Check (STRICT)

ALL of the following must be true:
1. Phase 5 (validate) shows PASS for the thesis version being ratcheted
2. Zero PENDING invariants remain (all must be confirmed or explicitly removed)
3. The validation report shows 100% row parsing success
4. The analyst explicitly confirms the ratchet

If ANY gate fails: ERROR with specific failures listed.

### Execution Flow

1. **Verify ratchet readiness** (gate check above — hard fail if not met).

2. **Determine semver version**:
   - If no prior contract exists: `v1.0.0`
   - If prior contract exists: compute diff and bump appropriately:
     - New required fields → MAJOR bump
     - New optional fields → MINOR bump
     - Validator changes only → PATCH bump

3. **Copy thesis to contract directory**:
   - `artefacts/<domain>/6-contracts/v{semver}/contract.py` (from `draft.py`)
   - `artefacts/<domain>/6-contracts/v{semver}/contract.schema.json` (from `draft.schema.json`)
   - Add a header comment: `# Ratcheted: {timestamp} from thesis v{N}`

4. **Freeze** — the contract files are now immutable. Any future changes require a new version.

5. **Update state**:
   ```json
   {
     "contract_version": "1.0.0",
     "ratcheted_at": "<timestamp>",
     "ratcheted_from": "thesis_v3"
   }
   ```

6. **Write audit entry** recording the ratchet event with analyst confirmation.

7. **Report**: Contract version, location, readiness for `/adm.model`.

## Guidelines

- Ratcheting is a ONE-WAY operation. Double-check before confirming.
- The stability window (if configured) must have elapsed — this prevents premature ratcheting of a thesis that hasn't been tested enough.
- Zero PENDING invariants is non-negotiable. If an invariant is legitimately not applicable, it must be explicitly removed (with audit trail), not left as PENDING.
- After ratcheting, the thesis directory remains as historical record — don't delete it.
