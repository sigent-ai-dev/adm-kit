# Data Model: ADM Check

## Entities

### CheckFinding

A single observation from the validation process.

| Field | Type | Description |
|-------|------|-------------|
| severity | Severity (error/warning/info) | Determines exit code impact |
| domain | str | Which domain this finding applies to |
| message | str | Human-readable description |
| phase | int or None | Which phase this relates to (optional) |

### CheckReport

Aggregation of all findings for the project.

| Field | Type | Description |
|-------|------|-------------|
| findings | list[CheckFinding] | All collected findings |

**Derived properties:**
- `errors` → count of findings where severity == error
- `warnings` → count of findings where severity == warning
- `passed` → True when errors == 0

## State Transitions

None — `adm check` is read-only. It never modifies the state file or artefacts.

## Relationships

- CheckReport contains 0..N CheckFinding instances
- Each CheckFinding references a domain name from ProjectState.domains
- Phase references map to the PHASE_DIRS constant from init.py
