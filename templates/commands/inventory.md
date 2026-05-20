---
description: Catalogue every column of every file in the domain — Phase 2 of ADM.
handoffs:
  - label: Extract Invariants
    agent: adm.invariants
    prompt: Extract cross-cutting rules from the inventory
    send: true
---

## User Input

```text
$ARGUMENTS
```

## Outline

`/adm.inventory` is Phase 2. It produces a complete catalogue of every column in every file that belongs to this domain. This is the foundation for thesis construction.

### Gate Check

- Phase 1 (lineage) must be complete
- `artefacts/<domain>/1-lineage/lineage.json` must exist

### Execution Flow

1. **Load lineage** to understand source files and their roles.

2. **For each source file**, catalogue every column:
   ```markdown
   ### COL-NNN: <column_name>

   **File**: <source file>
   **Position**: [column index or cell reference]
   **Observed type**: [string | integer | float | date | boolean | mixed]
   **Sample values**: [3-5 representative values]
   **Null rate**: [percentage or "never null"]
   **Description**: [what this column represents — from headers, context, or inference]
   **Confidence**: [high | medium | low]
   **Notes**: [sentinel values, formatting quirks, derived-from references]
   ```

3. **Handle wide files** (>1000 columns):
   - If a file exceeds 1000 columns, raise a clarification:
     "This file has N columns. Options: (a) chunk into logical groups, (b) inventory first 1000, (c) skip and note. Which approach?"
   - If chunked: each chunk gets its own COL-NNN namespace prefix

4. **Cross-reference with lineage**:
   - Every column should trace to a source in lineage
   - Flag columns that appear in lineage but not in files (missing data)
   - Flag columns in files that don't appear in lineage (undocumented)

5. **Write artefacts** to `artefacts/<domain>/2-inventory/`:
   - `inventory.md` — human-readable catalogue
   - `inventory.json` — machine-readable (array of column objects)

6. **Update state** and **write audit entry**.

### Output Structure (inventory.json)

```json
{
  "domain": "<domain>",
  "total_columns": 142,
  "files": [
    {
      "name": "holdings.csv",
      "columns": [
        {
          "id": "COL-001",
          "name": "portfolio_id",
          "position": 0,
          "observed_type": "string",
          "sample_values": ["PF001", "PF002", "PF003"],
          "null_rate": 0.0,
          "description": "Unique portfolio identifier",
          "confidence": "high"
        }
      ]
    }
  ]
}
```

## Guidelines

- Completeness over depth. Every column must appear. Descriptions can be brief for obvious columns.
- Mark confidence honestly. A column named "X1" with no header gets `low` confidence.
- Preserve analyst resolutions from Phase 1 open questions — if CLR-001 resolved a column name, use that resolution.
- Don't infer types beyond what the data shows. "Looks like a date" is `observed_type: "string"` with a note "appears to be ISO date format".
