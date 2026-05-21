# Feature Specification: ADM Check — State Validation

**Feature Branch**: `feature/5-adm-check`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the `adm check` CLI command that validates ADM project state — schema integrity, artefact existence, invariant suite, and open clarifications.

## User Scenarios & Testing

### User Story 1 - Developer verifies project health (Priority: P1)

A developer runs `adm check` after completing work on a phase to confirm their project state is valid — the state file is well-formed, artefact directories exist for completed phases, and there are no structural issues blocking advancement.

**Why this priority**: This is the primary use case — a quick health check that catches issues before they compound across phases.

**Independent Test**: Run `adm check` against a valid project and verify it exits 0 with a clean report. Run against a project with a missing artefact directory and verify it exits non-zero with a specific error.

**Acceptance Scenarios**:

1. **Given** a valid project with one domain at phase 3, **When** `adm check` runs, **Then** it validates the state file, checks artefact dirs for phases 1-3, and exits 0 with a success summary.
2. **Given** a project where `artefacts/holdings/2-inventory/` is missing but state claims phase 3, **When** `adm check` runs, **Then** it reports the missing directory as an error and exits non-zero.
3. **Given** a project with no `.adm/project.json`, **When** `adm check` runs, **Then** it reports "No ADM project found" and exits non-zero.

---

### User Story 2 - Developer sees open clarification count (Priority: P2)

A developer runs `adm check` to see how many clarification questions (CLR-NNN) remain open across all domains, helping them understand what analyst work is still needed before ratcheting.

**Why this priority**: Visibility into open questions prevents surprises at ratchet time when zero-open-CLR is enforced.

**Independent Test**: Create a project with 2 open and 1 resolved CLR entries, run `adm check`, verify the report shows "2 open / 1 resolved".

**Acceptance Scenarios**:

1. **Given** a domain with 3 open and 2 resolved clarifications, **When** `adm check` runs, **Then** the report shows "3 open, 2 resolved" for that domain.
2. **Given** a domain with zero open clarifications, **When** `adm check` runs, **Then** it shows "Ready for ratchet" in the clarifications section.

---

### User Story 3 - Developer runs invariant suite (Priority: P2)

A developer whose domain is at Phase 3 or beyond runs `adm check` and it automatically executes the invariant pytest suite, reporting pass/fail counts as part of the health check.

**Why this priority**: Invariant regression detection is valuable but depends on Phase 3+ being complete — a secondary concern after basic structural validation.

**Independent Test**: Create a domain at phase 4 with an `invariants.py` in the artefacts, run `adm check`, verify it reports invariant test results.

**Acceptance Scenarios**:

1. **Given** a domain at phase 4 with `artefacts/<domain>/3-invariants/invariants.py`, **When** `adm check` runs, **Then** it executes the invariant suite and reports pass/fail counts.
2. **Given** a domain at phase 2 (before invariants), **When** `adm check` runs, **Then** it skips the invariant suite without error.
3. **Given** invariants that fail, **When** `adm check` runs, **Then** it reports failures as warnings (not blocking errors — only ratchet blocks on invariant failures).

---

### Edge Cases

- What happens if `.adm/project.json` exists but is corrupt JSON? Report a schema validation error with details.
- What happens if a domain's `current_phase` is higher than the artefact directories that exist? Report missing phases.
- What happens if `invariants.py` has import errors? Report the import failure, don't crash.
- What about multi-domain projects? Check each domain independently and report all results.

## Requirements

### Functional Requirements

- **FR-001**: `adm check` MUST validate `.adm/project.json` against the Pydantic state schema and report structural errors
- **FR-002**: `adm check` MUST verify artefact directories exist for all phases up to and including `current_phase` for each domain
- **FR-003**: `adm check` MUST report unresolved clarification questions (CLR-NNN with status "open") per domain
- **FR-004**: `adm check` MUST run the invariant pytest suite if the domain is at Phase 3 or beyond and `invariants.py` exists
- **FR-005**: `adm check` MUST exit with code 0 if all checks pass, non-zero if any errors are found
- **FR-006**: `adm check` MUST produce rich-formatted output with severity-coloured findings (error=red, warning=yellow, info=dim)
- **FR-007**: `adm check` MUST check all domains in a multi-domain project independently
- **FR-008**: `adm check` MUST report a summary at the end showing total errors, warnings, and pass status

### Key Entities

- **Check Result**: A finding from the validation process with severity (error, warning, info) and description
- **Domain Report**: Collection of check results for a single domain
- **Project Report**: Aggregation of all domain reports with overall pass/fail status

## Success Criteria

### Measurable Outcomes

- **SC-001**: `adm check` completes in under 5 seconds for a project with up to 10 domains (excluding invariant test runtime)
- **SC-002**: All structural issues (missing dirs, invalid state) are detected with zero false negatives
- **SC-003**: Output clearly shows which domain and which phase has an issue — developers can fix problems without further investigation
- **SC-004**: Exit code is reliable for CI integration (0 = clean, non-zero = issues)

## Assumptions

- The state schema from issue #1 is available and the state file is loaded via `load_state()`
- Phase template YAML frontmatter defines `expected_outputs` but check does NOT validate individual file existence within phase dirs (only directory existence for now)
- Invariant suite execution is optional — if `invariants.py` doesn't exist, it's not an error
- The check command operates on the current working directory (finds `.adm/project.json` from cwd)
- Warnings (open CLRs, invariant failures) don't cause non-zero exit — only errors do
