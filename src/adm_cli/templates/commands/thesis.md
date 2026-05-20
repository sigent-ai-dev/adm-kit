---
description: Produce a candidate schema as a falsifiable claim — Phase 4 of ADM.
handoffs:
  - label: Validate Thesis
    agent: adm.validate
    prompt: Run validation against real snapshots
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.thesis` is Phase 4. It produces a candidate Pydantic model that claims to describe this domain's data. The thesis is a HYPOTHESIS — it will be tested in Phase 5.

### Gate Check

- Phase 3 (invariants) must be complete
- `artefacts/<domain>/3-invariants/invariants.json` must exist
- All open questions from Phase 1 that impact schema must be resolved

### Execution Flow

1. **Load all prior artefacts** (lineage, inventory, invariants).

2. **Determine version**: Check for existing theses in `artefacts/<domain>/4-thesis/`. New thesis goes in `v{N+1}/`.

3. **Construct the Pydantic model**:
   - Map each COL-NNN from inventory to a typed field
   - Apply invariants as validators where possible
   - Use `Optional[T]` only where nullability is confirmed
   - Use `Literal[...]` for known enum values
   - Use `Annotated[T, Field(...)]` for constraints (min, max, pattern)

4. **Write thesis narrative** explaining the claim:
   ```markdown
   # Thesis v{N} — <domain>

   ## Claim
   This Pydantic model correctly describes the <domain> data domain as
   observed in [source files]. It encodes [N] fields, [M] validators,
   and satisfies all [K] confirmed invariants from Phase 3.

   ## Key design decisions
   - [Why field X is typed as Y]
   - [Why these fields are optional]
   - [How business rule Z is encoded]

   ## Known limitations
   - [What this thesis doesn't capture yet]
   - [Pending invariants that aren't encoded]

   ## Falsification targets
   - [Specific scenarios that would prove this thesis wrong]
   - [Edge cases to test in validation]
   ```

5. **Write artefacts** to `artefacts/<domain>/4-thesis/v{N}/`:
   - `thesis.md` — narrative claim
   - `draft.py` — Pydantic model
   - `draft.schema.json` — derived JSON Schema

6. **Update state** (increment iteration counter) and **write audit entry**.

## Guidelines

- A thesis is a CLAIM, not a final answer. Write it to be falsified.
- The Pydantic model should be strict by default — reject data that doesn't conform rather than silently coercing.
- Include `model_config = ConfigDict(strict=True)` unless there's a reason not to.
- Name fields clearly using the domain vocabulary from lineage, not the raw column names (unless they're already clear).
- If the inventory has low-confidence columns, include them with a comment noting the uncertainty.
- Each iteration should explain what changed from the previous version.
