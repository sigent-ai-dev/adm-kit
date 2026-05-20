---
phase: 2
name: inventory
expected_outputs:
  - filename: inventory.md
    format: md
    required: true
  - filename: inventory.json
    format: json
    required: true
versioned: false
depends_on:
  phase: 1
  artefacts:
    - lineage.md
    - lineage.json
---

# Phase 2: Inventory

## Purpose

Catalogue every column of every file in the data domain. The inventory is exhaustive — nothing is skipped, nothing is assumed. Each column gets a unique identifier (COL-NNN) and a semantic description.

## Inputs

- Source data file(s) (the actual CSV/XLSX/XML/etc.)
- `lineage.md` and `lineage.json` from Phase 1 (context on what the data represents)

## Process

1. **Extract column list** — programmatically list every column/field in the source
2. **Assign identifiers** — each column gets a COL-NNN code (sequential, zero-padded)
3. **Describe semantics** — what does this column represent in business terms?
4. **Classify data type** — observed type (string, integer, decimal, date, boolean, etc.)
5. **Note anomalies** — nulls, mixed types, sentinel values, encoding issues
6. **Raise clarifications** — where column semantics are unclear, raise CLR-NNN questions

For wide files (>1000 columns), chunk into groups and process iteratively.

## Outputs

### `inventory.md`

Human-readable catalogue:

| ID | Column Name | Semantic Description | Type | Nullable | Notes |
|----|-------------|---------------------|------|----------|-------|
| COL-001 | account_id | Unique account identifier | string | No | Format: ACC-NNNN |
| COL-002 | balance | Current balance in GBP | decimal | No | 2dp precision |
| ... | ... | ... | ... | ... | ... |

### `inventory.json`

Machine-readable catalogue:

```json
{
  "domain": "<domain-name>",
  "source_file": "<filename>",
  "column_count": 42,
  "columns": [
    {
      "id": "COL-001",
      "name": "account_id",
      "description": "Unique account identifier",
      "type": "string",
      "nullable": false,
      "notes": "Format: ACC-NNNN"
    }
  ]
}
```

## Completion Criteria

- Every column in the source data is catalogued (zero omissions)
- Each column has a COL-NNN identifier
- Each column has a semantic description (not just the raw column name)
- Data types are observed from actual data, not assumed
- Anomalies and sentinel values are noted
- Both `inventory.md` and `inventory.json` are consistent
- Column count in JSON matches actual source column count
