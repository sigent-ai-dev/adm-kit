# Tasks: ADM Check — State Validation

**Input**: Design documents from `specs/005-adm-check/`

**Prerequisites**: plan.md (required), spec.md (required), data-model.md

**Tests**: Included — this is a core CLI command that needs test coverage for CI reliability.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create the check module and wire it into the CLI

- [ ] T001 Create `src/adm_cli/check.py` with `Severity` enum (error/warning/info), `CheckFinding` dataclass, and `CheckReport` class
- [ ] T002 Wire check command into typer app in `src/adm_cli/__init__.py` (replace stub with import from check module)

---

## Phase 2: Foundational

**Purpose**: Core validation logic that all user stories depend on

- [ ] T003 Implement state file validation in `src/adm_cli/check.py` — load `.adm/project.json` via `load_state()`, catch `ValidationError`, report as error finding
- [ ] T004 Implement "no project found" detection — if `.adm/project.json` doesn't exist, report error and exit early

**Checkpoint**: `adm check` can detect missing/corrupt state files.

---

## Phase 3: User Story 1 — Developer verifies project health (Priority: P1) 🎯 MVP

**Goal**: Validate state file integrity and artefact directory existence for all domains.

**Independent Test**: Run `adm check` against a valid project → exit 0. Run against a project with missing artefact dir → exit 1.

### Implementation for User Story 1

- [ ] T005 [US1] Implement artefact directory validation — for each domain, verify `artefacts/<domain>/<N>-<phase>/` exists for phases 1 through `current_phase` in `src/adm_cli/check.py`
- [ ] T006 [US1] Implement rich-formatted output — print findings with severity colours (error=red, warning=yellow, info=dim) and domain/phase context in `src/adm_cli/check.py`
- [ ] T007 [US1] Implement exit code logic — exit 0 if zero errors, exit 1 if any errors in `src/adm_cli/check.py`
- [ ] T008 [US1] Implement summary line — "N errors, M warnings — PASS/FAIL" at end of output in `src/adm_cli/check.py`
- [ ] T009 [P] [US1] Test: valid project exits 0 in `tests/test_check.py`
- [ ] T010 [P] [US1] Test: missing artefact directory reports error and exits non-zero in `tests/test_check.py`
- [ ] T011 [P] [US1] Test: missing state file reports error in `tests/test_check.py`
- [ ] T012 [P] [US1] Test: corrupt state file reports schema validation error in `tests/test_check.py`

**Checkpoint**: `adm check` validates structural health for any project. MVP complete.

---

## Phase 4: User Story 2 — Open clarification count (Priority: P2)

**Goal**: Report open CLR-NNN questions per domain.

**Independent Test**: Create project with open/resolved CLRs, verify report shows counts.

### Implementation for User Story 2

- [ ] T013 [US2] Implement clarification reporting — count open vs resolved in `domain.resolutions`, emit warning for open, info for "ready for ratchet" in `src/adm_cli/check.py`
- [ ] T014 [P] [US2] Test: domain with open CLRs shows warning with count in `tests/test_check.py`
- [ ] T015 [P] [US2] Test: domain with zero open CLRs shows "ready for ratchet" in `tests/test_check.py`

**Checkpoint**: Developers can see CLR status at a glance.

---

## Phase 5: User Story 3 — Invariant suite execution (Priority: P2)

**Goal**: Run invariant pytest suite for domains at Phase 3+ and report results.

**Independent Test**: Create domain at phase 4 with invariants.py, verify check reports pass/fail counts.

### Implementation for User Story 3

- [ ] T016 [US3] Implement invariant suite runner — subprocess `python -m pytest <path> --tb=short -q`, parse exit code and output, emit warning on failures in `src/adm_cli/check.py`
- [ ] T017 [US3] Implement phase-gate skip — only run invariants if `current_phase >= 3` AND `invariants.py` exists in `src/adm_cli/check.py`
- [ ] T018 [P] [US3] Test: domain at phase 4 with invariants runs suite in `tests/test_check.py`
- [ ] T019 [P] [US3] Test: domain at phase 2 skips invariant suite in `tests/test_check.py`
- [ ] T020 [P] [US3] Test: invariant failures reported as warnings (not errors) in `tests/test_check.py`

**Checkpoint**: Full check command operational with invariant support.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Multi-domain support and `--domain` flag

- [ ] T021 Implement `--domain` optional flag to check a single domain in `src/adm_cli/check.py`
- [ ] T022 Implement multi-domain iteration — check each domain independently, aggregate findings in `src/adm_cli/check.py`
- [ ] T023 [P] Test: multi-domain project checks all domains in `tests/test_check.py`
- [ ] T024 [P] Test: `--domain` flag restricts to single domain in `tests/test_check.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Story 1 (Phase 3)**: Depends on Phase 2 — BLOCKS MVP delivery
- **User Story 2 (Phase 4)**: Depends on Phase 2 only (independent of US1)
- **User Story 3 (Phase 5)**: Depends on Phase 2 only (independent of US1/US2)
- **Polish (Phase 6)**: Depends on US1 completion

### Parallel Opportunities

```
After Phase 2 completes:
  T005-T008 (US1 implementation) — sequential
  T009, T010, T011, T012 (US1 tests) — all [P]
  T013 (US2) — independent of US1
  T016-T017 (US3) — independent of US1/US2
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. T001-T002: Setup
2. T003-T004: Foundational
3. T005-T012: User Story 1 (state + artefact validation)
4. **STOP and VALIDATE**: `adm check` works for basic health checks

### Full Delivery

1. MVP above
2. T013-T015: CLR reporting
3. T016-T020: Invariant execution
4. T021-T024: Multi-domain polish

---

## Summary

- **Total tasks**: 24
- **Task count per story**: US1=8, US2=3, US3=5, Setup=2, Foundation=2, Polish=4
- **Parallel tasks**: 11 (all tests + independent story starts)
- **MVP scope**: T001-T012 (12 tasks)
- **Format validation**: All tasks follow checklist format (checkbox, ID, labels, file paths) ✓
