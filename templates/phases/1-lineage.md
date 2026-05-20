---
phase: 1
name: lineage
expected_outputs:
  - filename: lineage.md
    format: md
    required: true
  - filename: lineage.json
    format: json
    required: true
versioned: false
depends_on:
  phase: 0
  artefacts:
    - source data file(s)
---

# Phase 1: Lineage

## Purpose

Trace the full lifecycle of the data domain — where it originates, what systems touch it, what mutations occur, and what business processes depend on it. Lineage establishes the context that all subsequent phases build upon.

## Inputs

- Source data file(s) (CSV, XLSX, XML, database export, etc.)
- Domain knowledge from stakeholders (optional but valuable)
- Existing documentation (data dictionaries, ERDs, wiki pages)

## Process

1. **Identify the source** — where does this data originate? (system, manual entry, external feed)
2. **Trace the lifecycle** — what systems touch it between origin and current state?
3. **Document mutations** — what transforms, enrichments, or aggregations occur?
4. **Map consumers** — who/what reads this data and for what purpose?
5. **Surface open questions** — where is the lifecycle unclear? Raise CLR-NNN questions.

## Outputs

### `lineage.md`

Human-readable narrative covering:
- **Origin** — source system, frequency, format
- **Touchpoints** — each system/process that reads or writes this data
- **Mutations** — transformations applied at each touchpoint
- **Consumers** — downstream systems and their dependencies
- **Open Questions** — CLR-NNN items for unclear data flows

### `lineage.json`

Machine-readable structured representation:

```json
{
  "domain": "<domain-name>",
  "origin": {
    "system": "<source-system>",
    "format": "<file-format>",
    "frequency": "<how-often>"
  },
  "touchpoints": [
    {
      "system": "<system-name>",
      "operation": "read|write|transform",
      "description": "<what-happens>"
    }
  ],
  "consumers": [
    {
      "system": "<system-name>",
      "purpose": "<why-it-reads-this-data>"
    }
  ],
  "open_questions": [
    {
      "id": "CLR-001",
      "question": "<what-is-unclear>",
      "context": "<why-it-matters>"
    }
  ]
}
```

## Completion Criteria

- All known data touchpoints are documented
- Origin system and format are identified
- At least one consumer is documented
- Open questions are raised for any unclear data flows (not necessarily resolved — that's the clarify gate's job)
- Both `lineage.md` and `lineage.json` are consistent with each other
