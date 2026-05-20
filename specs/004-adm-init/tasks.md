# Tasks: Implement `adm init`

**Input**: Design documents from `specs/004-adm-init/`

**Prerequisites**: plan.md, spec.md, schema.py (issue #1)

## Phase 1: Setup

- [ ] T001 Add `source_path` optional field to `DomainState` in `src/adm_cli/schema.py`
- [ ] T002 Create `src/adm_cli/templates/` package with `__init__.py`
- [ ] T003 Copy command and phase templates into `src/adm_cli/templates/` as package data
- [ ] T004 Update `pyproject.toml` hatch build config to include `templates/` as package data

---

## Phase 2: Foundational

- [ ] T005 Create `src/adm_cli/init.py` with the init command implementation
- [ ] T006 Wire init command into the typer app in `src/adm_cli/__init__.py` (replace stub)

---

## Phase 3: User Story 1 — Initialise new domain (Priority: P1)

**Goal**: `adm init holdings --source ./data/file.csv` creates complete scaffolding.

### Implementation

- [ ] T007 [US1] Implement state file creation (load or create `.adm/project.json`, add domain entry)
- [ ] T008 [US1] Implement artefact directory creation (`artefacts/<domain>/1-lineage/` through `7-model/`)
- [ ] T009 [US1] Implement command file installation (copy from package data to agent directory with `adm.` prefix)
- [ ] T010 [US1] Implement success summary output (rich table showing what was created)

---

## Phase 4: User Story 2 — Multi-domain support (Priority: P1)

**Goal**: Adding a second domain is additive, re-init is blocked without `--force`.

### Implementation

- [ ] T011 [US2] Implement domain-exists check with `--force` override
- [ ] T012 [US2] Ensure existing domains are preserved when adding new ones

---

## Phase 5: User Story 3 — Multi-agent support (Priority: P2)

**Goal**: `--ai` flag installs to the correct agent directory.

### Implementation

- [ ] T013 [US3] Implement agent directory mapping (claude, gemini, copilot, cursor, q, windsurf)
- [ ] T014 [US3] Default to claude when `--ai` not specified

---

## Phase 6: Tests

- [ ] T015 [P] Test: init creates state file with correct domain entry
- [ ] T016 [P] Test: init creates all 7 artefact directories
- [ ] T017 [P] Test: init installs command files to agent directory
- [ ] T018 [P] Test: init refuses re-init without --force
- [ ] T019 [P] Test: init with --force resets domain to phase 1
- [ ] T020 [P] Test: multi-domain is additive
- [ ] T021 [P] Test: --ai flag installs to correct directory

---

## Dependencies

- T001-T004: Setup (parallel-safe)
- T005-T006: After setup
- T007-T010: After T005-T006
- T011-T012: After T007
- T013-T014: After T009
- T015-T021: After all implementation (parallel)

## Summary

- **Total tasks**: 21
- **Parallel tasks**: 7 (tests)
- **Estimated effort**: M (3-5 days)
