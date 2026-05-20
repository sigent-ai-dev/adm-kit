---
description: Trace data lifecycle, touchpoints, mutations, and open questions — Phase 1 of ADM.
handoffs:
  - label: Run Inventory
    agent: adm.inventory
    prompt: Catalogue every column of every file for this domain
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.lineage` is Phase 1. It traces how data flows through the system — where it originates, what transforms it, where it's consumed, and what validation points exist.

### Gate Check

- `.adm/project.json` must exist (run `adm init <domain>` first)
- Source data path must be accessible

### Execution Flow

1. **Identify the domain** from state or user input.

2. **Trace the data lifecycle**:
   - **Sources**: Where does this data originate? (upstream systems, files, APIs)
   - **Touchpoints**: What systems read or write this data?
   - **Mutations**: Where does the data shape change? (formulas, joins, filters, aggregations)
   - **Validation points**: Where is data currently checked? (spreadsheet validation rules, SQL constraints, VBA assertions)
   - **Consumers**: Who/what uses the final output?

3. **Identify open questions**:
   For anything unclear from the data alone — ambiguous column names, undocumented formulas, sentinel values without documentation — raise as a structured clarification:
   ```markdown
   ### OQ-NNN
   **Column/Cell**: [reference]
   **Question**: [what's unclear]
   **Impact**: [what downstream phases need this answer for]
   **Resolution**: [OPEN]
   ```

4. **Write artefacts** to `artefacts/<domain>/1-lineage/`:
   - `lineage.md` — human-readable narrative
   - `lineage.json` — machine-readable structured data

5. **Update state** and **write audit entry**.

### Output Structure (lineage.json)

```json
{
  "domain": "<domain>",
  "sources": [
    { "name": "...", "format": "...", "cadence": "...", "description": "..." }
  ],
  "touchpoints": [
    { "system": "...", "role": "producer|consumer|transformer", "description": "..." }
  ],
  "mutations": [
    { "location": "...", "type": "formula|join|filter|aggregation", "description": "..." }
  ],
  "validation_points": [
    { "location": "...", "rule": "...", "enforced": true }
  ],
  "open_questions": [
    { "id": "OQ-001", "column": "...", "question": "...", "impact": "...", "status": "open" }
  ]
}
```

## Guidelines

- This phase is DISCOVERY, not design. Document what IS, not what should be.
- Err on the side of raising open questions — unasked questions become bugs in Phase 4.
- If source data isn't available, work from documentation, screenshots, or analyst descriptions — but mark confidence levels.
- The lineage should be understandable by a domain analyst, not just an engineer.
