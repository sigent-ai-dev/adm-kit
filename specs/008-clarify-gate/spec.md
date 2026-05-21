# Feature Specification: Clarify-Gate Pattern

**Feature Branch**: `feature/8-clarify-gate`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the clarify-gate pattern — structured CLR-NNN questions that persist across phase re-runs, with merge behaviour control.

## User Scenarios & Testing

### User Story 1 - AI agent raises clarification during phase execution (Priority: P1)

An AI agent running `/adm.lineage` encounters an ambiguous column name. It raises a structured CLR-NNN question that gets stored in the domain's state. When the phase is re-run later (with new data or after resolving questions), existing resolutions are preserved.

**Why this priority**: This is the core mechanism — without it, analyst decisions get lost on every re-run, violating the "preserve analyst work" principle.

**Independent Test**: Raise a CLR, resolve it, re-run the phase, verify the resolution survives.

**Acceptance Scenarios**:

1. **Given** a domain with no resolutions, **When** a new CLR-001 question is raised, **Then** it appears in `domain.resolutions` with status "open".
2. **Given** CLR-001 is resolved, **When** the phase is re-run and raises CLR-001 again, **Then** the existing resolution is preserved (merge behaviour).
3. **Given** CLR-001 is resolved and CLR-002 is new, **When** the phase re-runs, **Then** CLR-001 stays resolved and CLR-002 is added as open.

---

### User Story 2 - Developer controls merge behaviour with --resolutions flag (Priority: P1)

A developer re-running a phase can choose how new questions interact with existing resolutions: merge (default — preserve existing), overwrite (discard all, re-raise fresh), or skip (don't raise any new questions).

**Why this priority**: Different re-run scenarios need different behaviour. Fresh data may invalidate old answers (overwrite), while minor updates should preserve work (merge).

**Independent Test**: Run with each flag value and verify the expected merge behaviour.

**Acceptance Scenarios**:

1. **Given** existing resolutions and `--resolutions merge` (default), **When** new CLRs are raised, **Then** existing resolutions are kept, new questions are added as open.
2. **Given** existing resolutions and `--resolutions overwrite`, **When** new CLRs are raised, **Then** all prior resolutions are discarded, all questions are fresh and open.
3. **Given** existing resolutions and `--resolutions skip`, **When** the phase runs, **Then** no new questions are raised, only existing resolutions are used.

---

### User Story 3 - adm check reports clarification status (Priority: P2)

A developer runs `adm check` and sees the count of open vs resolved clarifications per domain, giving visibility into analyst work remaining before ratcheting.

**Why this priority**: Already partially implemented in issue #5 — this story ensures the clarify module integrates cleanly with the existing check command.

**Independent Test**: Already covered by test_check.py (CLR reporting tests from issue #5).

**Acceptance Scenarios**:

1. **Given** 3 open and 2 resolved CLRs, **When** `adm check` runs, **Then** it reports "3 open, 2 resolved" as a warning.
2. **Given** zero open CLRs, **When** `adm check` runs, **Then** it reports "ready for ratchet".

---

### Edge Cases

- CLR-NNN IDs must be globally unique within a domain — never reused even if the question is removed.
- What if a resolution references a column that no longer exists after data refresh? The resolution is still preserved (analyst decides if it's still valid).
- Maximum number of CLRs per domain? No limit — but `adm status` shows the count.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST support structured clarification questions with format: ID (CLR-NNN), question text, context, resolution status (open/resolved)
- **FR-002**: Resolutions MUST be stored in `.adm/project.json` under `domain.resolutions` as a `{CLR-ID: status}` mapping
- **FR-003**: Re-running a phase MUST preserve existing resolutions by default (merge behaviour)
- **FR-004**: The `--resolutions` flag MUST support three modes: `merge` (default), `overwrite`, `skip`
- **FR-005**: CLR-NNN IDs MUST be globally unique within a domain and never reused
- **FR-006**: The system MUST provide a function to raise a new CLR question (returns the next available ID)
- **FR-007**: The system MUST provide a function to resolve a CLR by ID (sets status to "resolved" with answer text)
- **FR-008**: `adm check` MUST report open vs resolved counts per domain (already implemented in issue #5)

### Key Entities

- **Clarification (CLR)**: A structured question raised during phase execution with ID, question, context, and status
- **Resolution**: The analyst's answer to a CLR, persisted in the state file
- **Merge Mode**: Controls how new CLRs interact with existing resolutions on phase re-run

## Success Criteria

### Measurable Outcomes

- **SC-001**: Resolutions survive 100% of phase re-runs under default (merge) behaviour
- **SC-002**: No analyst decision is ever silently discarded without explicit `--resolutions overwrite`
- **SC-003**: The next available CLR-NNN ID is always correctly computed (no collisions)
- **SC-004**: All three merge modes produce the expected state after re-run

## Assumptions

- The state schema already has `resolutions: dict[str, ResolutionStatus]` (implemented in issue #1)
- Resolution status is either "open" or "resolved" (the ResolutionStatus enum already exists)
- The actual question text and context are stored in artefact files (not in project.json — only the ID and status live in state)
- The `--resolutions` flag is passed to phase commands, not to `adm check` or `adm status`
- CLR IDs are sequential within a domain: CLR-001, CLR-002, etc.
