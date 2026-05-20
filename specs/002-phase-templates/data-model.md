# Data Model: Phase Artefact Templates

## Entities

### PhaseTemplate

A markdown file with YAML frontmatter that defines one ADM phase's expected artefacts.

| Field | Type | Description |
|-------|------|-------------|
| phase | int (1-7) | Phase number |
| name | string | Phase name (lineage, inventory, etc.) |
| expected_outputs | list[OutputSpec] | Files this phase produces |
| versioned | bool | Whether outputs live in version subdirectories |
| versioning | string? | "iteration" or "semver" (null if not versioned) |
| depends_on.phase | int | Prior phase number |
| depends_on.artefacts | list[string] | Required files from prior phase |

### OutputSpec

| Field | Type | Description |
|-------|------|-------------|
| filename | string | Expected output filename |
| format | string | File format: md, json, py |
| required | bool | Whether file must exist for phase completion |

## Relationships

- Each PhaseTemplate depends on exactly one prior phase (except phase 1 which depends on source data)
- PhaseTemplate.expected_outputs defines what `adm check` validates
- Phase 4 and 5 templates have `versioned: true` with `versioning: iteration`
- Phase 6 template has `versioned: true` with `versioning: semver`
