# Feature Specification: ADM Status — Progression Display

**Feature Branch**: `feature/6-adm-status`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the `adm status` CLI command that displays a Rich table showing per-domain phase progression.

## User Scenarios & Testing

### User Story 1 - Developer checks domain progress at a glance (Priority: P1)

A developer runs `adm status` to see a formatted table of all domains and their current phase, iteration count, contract version, and open question count — giving a complete picture of project progress without opening any files.

**Why this priority**: This is the only use case — a quick dashboard view. The command is simple but high-visibility.

**Independent Test**: Create a project with 2 domains at different phases, run `adm status`, verify the table renders with correct data for both.

**Acceptance Scenarios**:

1. **Given** a project with domain "holdings" at phase 4 iteration 2 with 3 open questions, **When** `adm status` runs, **Then** the table shows: Domain=holdings, Phase="4 — Thesis", Iteration=2, Contract=—, Open Questions=3.
2. **Given** a project with domain "cashflows" that has contract v1.0.0 and zero open questions, **When** `adm status` runs, **Then** the table shows: Domain=cashflows, Phase="7 — Model", Iteration=1, Contract=v1.0.0, Open Questions=0.
3. **Given** a project with no domains initialised, **When** `adm status` runs, **Then** it shows a guidance message: "No domains found. Run `adm init <domain>` to get started."

---

### Edge Cases

- What happens if `.adm/project.json` doesn't exist? Show "No ADM project found" and suggest `adm init`.
- What happens if state file is corrupt? Show error (delegate to same validation as `adm check`).

## Requirements

### Functional Requirements

- **FR-001**: `adm status` MUST display a Rich table with columns: Domain, Phase, Iteration, Contract Version, Open Questions
- **FR-002**: The Phase column MUST show both number and name (e.g., "4 — Thesis")
- **FR-003**: `adm status` MUST show all domains from `.adm/project.json`
- **FR-004**: Contract Version MUST display the version string or "—" if none
- **FR-005**: Open Questions MUST show the count of resolutions with status "open"
- **FR-006**: `adm status` MUST handle empty projects (no domains) with a guidance message
- **FR-007**: `adm status` MUST handle missing state file gracefully with error message

### Key Entities

- **Status Row**: One row per domain containing phase, iteration, contract version, open question count
- **Phase Name Map**: Mapping from phase number (1-7) to human-readable name

## Success Criteria

### Measurable Outcomes

- **SC-001**: `adm status` completes in under 1 second for up to 50 domains
- **SC-002**: A developer can understand their project's state in a single glance without scrolling
- **SC-003**: The output is informative enough that developers don't need to open `.adm/project.json` manually

## Assumptions

- The state schema from issue #1 provides all data needed (current_phase, iteration, contract_version, resolutions)
- Phase names are: 1=Lineage, 2=Inventory, 3=Invariants, 4=Thesis, 5=Validate, 6=Ratchet, 7=Model
- The command is read-only — it never modifies state
- No `--domain` filter needed (this is a quick overview command)
