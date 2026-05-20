---
phase: 7
name: model
expected_outputs:
  - filename: feature.json
    format: json
    required: true
  - filename: spec.md
    format: md
    required: true
versioned: false
depends_on:
  phase: 6
  artefacts:
    - contract.py
    - contract.schema.json
---

# Phase 7: Model

## Purpose

Hand off the ratcheted contract to Spec Kit by seeding a feature directory. This bridges ADM (data discovery) to Spec Kit (feature implementation). The contract's fields become entity definitions; invariants become acceptance criteria seeds.

## Inputs

- `contract.py` from Phase 6 (the frozen Pydantic model)
- `contract.schema.json` from Phase 6 (machine-readable schema)
- `invariants.md` from Phase 3 (for acceptance criteria seeds)
- `lineage.md` from Phase 1 (for context in the spec)

## Process

1. **Create feature directory** — `specs/NNN-<domain>-engine/`
2. **Generate `feature.json`** — metadata linking back to the ADM contract
3. **Generate `spec.md`** — a Spec Kit-compatible feature specification seeded from the contract
4. **Map fields to entities** — each contract field becomes an entity attribute
5. **Map invariants to AC** — each invariant becomes an acceptance criterion seed
6. **Establish traceability** — every spec requirement links to its source contract field

## Outputs

### `feature.json`

Metadata for Spec Kit integration:

```json
{
  "name": "<domain>-engine",
  "source": "adm-kit",
  "domain": "<domain-name>",
  "contract_version": "1.0.0",
  "contract_path": "artefacts/<domain>/6-contracts/v1.0.0/contract.py",
  "schema_path": "artefacts/<domain>/6-contracts/v1.0.0/contract.schema.json",
  "generated": "2026-05-20"
}
```

### `spec.md`

A Spec Kit feature specification seeded from the contract:

```markdown
# Feature Specification: <Domain> Engine

## Context

[From lineage.md — why this domain is being modelled]

## Key Entities

[From contract.py — each model class becomes an entity with attributes]

## Functional Requirements

[From contract fields — each field implies a storage/retrieval requirement]

## Acceptance Criteria

[From invariants — each INV-NNN becomes a testable AC]

## Traceability

| Requirement | Source | Contract Field |
|-------------|--------|---------------|
| FR-001 | INV-001 | account_id uniqueness |
```

## Completion Criteria

- `feature.json` references the correct contract version and paths
- `spec.md` is a valid Spec Kit feature specification (consumable by `/speckit.plan`)
- Every contract field is represented in the spec entities
- Every invariant has a corresponding acceptance criterion
- Traceability table maps every requirement to its contract source
- The feature directory is placed in the project's `specs/` directory
- Spec Kit commands (`/speckit.plan`, `/speckit.tasks`) can consume the output
