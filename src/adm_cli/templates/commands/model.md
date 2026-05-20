---
description: Hand off a ratcheted contract to Spec Kit by seeding a feature directory — Phase 7 of ADM.
handoffs:
  - label: Specify Feature (Spec Kit)
    agent: speckit.specify
    prompt: Create a specification for this data engine feature
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.model` is Phase 7 — the formal hand-off from ADM to Spec Kit. It reads a ratcheted contract and seeds a Spec Kit feature directory with the information needed to implement the data engine.

### Gate Check

- Phase 6 (ratchet) must be complete
- `artefacts/<domain>/6-contracts/v{semver}/contract.py` must exist

### Execution Flow

1. **Load the ratcheted contract** (latest version or user-specified).

2. **Generate feature metadata** (`feature.json`):
   ```json
   {
     "name": "<domain>-engine",
     "source": "adm-ratchet",
     "contract_version": "1.0.0",
     "domain": "<domain>",
     "fields": [...],
     "invariants": [...],
     "generated_at": "<timestamp>"
   }
   ```

3. **Generate spec seed** (`spec.md`):
   - Title: "Implement <domain> data engine"
   - Requirements derived from contract fields
   - Acceptance criteria derived from invariants
   - Quality attributes from the original intent (if Intent Kit was used upstream)

4. **Write to Spec Kit location**:
   - `specs/NNN-<domain>-engine/feature.json`
   - `specs/NNN-<domain>-engine/spec.md`

5. **Update state** (mark Phase 7 complete) and **write audit entry**.

6. **Report**: Feature directory path, readiness for `/speckit.plan`.

## Guidelines

- This is a HANDOFF, not an implementation. Don't write application code — write the seed that Spec Kit will consume.
- Map contract fields to entities and requirements in a way that's natural for feature development.
- Invariants become acceptance criteria — "the system MUST enforce INV-003" becomes a testable requirement.
- If Intent Kit was used upstream, reference the intent ID in the generated spec.
