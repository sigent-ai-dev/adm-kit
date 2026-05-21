# Feature Specification: Phase Gate Enforcement

**Feature Branch**: `feature/7-phase-gates`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement phase gate enforcement in the state manager — `can_advance()` and `advance_phase()` functions that validate prior phase completion before allowing advancement.

## User Scenarios & Testing

### User Story 1 - State manager enforces phase ordering (Priority: P1)

An AI agent or CLI command attempts to advance a domain's phase. The state manager validates that the prior phase's artefacts exist before allowing advancement, ensuring no phase can be skipped.

**Why this priority**: Phase gates are a core ADM principle. Without enforcement, the methodology's guarantees collapse.

**Independent Test**: Attempt to advance from phase 1 to 2 when `artefacts/<domain>/1-lineage/` has no expected output files → blocked. Create the files → allowed.

**Acceptance Scenarios**:

1. **Given** a domain at phase 1 with `lineage.md` and `lineage.json` present in the artefact directory, **When** `can_advance("holdings", 2)` is called, **Then** it returns True.
2. **Given** a domain at phase 1 with no artefact files, **When** `can_advance("holdings", 2)` is called, **Then** it returns False with a reason explaining what's missing.
3. **Given** a domain at phase 5 with zero PENDING invariants, **When** `can_advance("holdings", 6)` is called, **Then** it returns True (ratchet gate satisfied).
4. **Given** a domain at phase 5 with PENDING invariants remaining, **When** `can_advance("holdings", 6)` is called, **Then** it returns False explaining that PENDING invariants must be resolved.
5. **Given** `can_advance` returns True, **When** `advance_phase("holdings")` is called, **Then** `current_phase` is incremented by 1 and state is saved atomically.

---

### Edge Cases

- Attempting to advance beyond phase 7 — should return False.
- Attempting to advance to a non-sequential phase (e.g., jump from 2 to 5) — should return False.
- Domain doesn't exist — should raise an error.

## Requirements

### Functional Requirements

- **FR-001**: State manager MUST expose `can_advance(domain, target_phase) -> (bool, str)` returning success/failure with reason
- **FR-002**: Phase N+1 requires the prior phase's artefact directory to contain at least the required files from the phase template's `expected_outputs` frontmatter
- **FR-003**: Phase 6 (ratchet) additionally requires zero PENDING invariants in the domain's resolutions
- **FR-004**: `advance_phase(domain)` MUST increment `current_phase` by exactly 1 and save state atomically
- **FR-005**: Advancement MUST be rejected if target phase != current_phase + 1 (no skipping)
- **FR-006**: Advancement MUST be rejected if target phase > 7

## Success Criteria

### Measurable Outcomes

- **SC-001**: Phase gates prevent 100% of invalid phase transitions (no false allows)
- **SC-002**: Valid transitions succeed without false blocks
- **SC-003**: Error messages name the specific missing artefacts or conditions

## Assumptions

- Phase template frontmatter (`expected_outputs` with `required: true`) defines what files must exist
- The state manager reads templates at runtime via `importlib.resources` (same as init)
- Only `required: true` outputs are checked — optional outputs don't block advancement
- The ratchet gate (zero PENDING) checks `domain.resolutions` for any value that is not "resolved"
