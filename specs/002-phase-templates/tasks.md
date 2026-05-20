# Tasks: Phase Artefact Templates

**Input**: Design documents from `specs/002-phase-templates/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md

**Tests**: Not requested — this is a template-only feature with no executable code.

**Organization**: Tasks grouped by user story for independent implementation.

## Phase 1: Setup

**Purpose**: Ensure directory exists and format conventions are established

- [ ] T001 Create `templates/phases/` directory (already exists but empty)
- [ ] T002 Establish YAML frontmatter schema convention (documented in plan.md)

---

## Phase 2: Foundational

**Purpose**: Create the template that all others follow as a pattern

- [ ] T003 Create `templates/phases/1-lineage.md` — the reference template that establishes the format for all subsequent templates

**Checkpoint**: Once the lineage template is done, remaining templates can be created in parallel following the same pattern.

---

## Phase 3: User Story 1 — Developer scaffolding (Priority: P1)

**Goal**: All 7 phase templates exist with correct frontmatter and documentation sections.

**Independent Test**: Run `ls templates/phases/` and verify 7 files exist; parse YAML frontmatter of each.

### Implementation for User Story 1

- [ ] T004 [P] [US1] Create `templates/phases/2-inventory.md` with expected outputs: `inventory.md`, `inventory.json`
- [ ] T005 [P] [US1] Create `templates/phases/3-invariants.md` with expected outputs: `invariants.md`, `invariants.py`, `invariants.json`
- [ ] T006 [P] [US1] Create `templates/phases/4-thesis.md` with versioned outputs: `thesis.md`, `draft.py`, `draft.schema.json`
- [ ] T007 [P] [US1] Create `templates/phases/5-validate.md` with versioned outputs: `report.md`, `report.json`
- [ ] T008 [P] [US1] Create `templates/phases/6-ratchet.md` with semver outputs: `contract.py`, `contract.schema.json`
- [ ] T009 [P] [US1] Create `templates/phases/7-model.md` with outputs: `feature.json`, `spec.md`

**Checkpoint**: All 7 templates exist. AI agents can read them to know what to produce.

---

## Phase 4: User Story 2 — AI agent consumption (Priority: P1)

**Goal**: Templates contain enough detail that an AI agent can produce conformant artefacts.

**Independent Test**: Give an AI agent only the template + sample data and verify it produces correct file structure.

### Implementation for User Story 2

- [ ] T010 [US2] Review and enhance all 7 templates to ensure Process sections give agents actionable instructions
- [ ] T011 [US2] Verify each template's Inputs section references the correct prior-phase artefacts

**Checkpoint**: Templates are agent-ready.

---

## Phase 5: User Story 3 — Phase gate validation (Priority: P2)

**Goal**: Templates' frontmatter is parseable by `adm check` for completeness validation.

**Independent Test**: Write a Python snippet that loads frontmatter from all 7 templates and extracts expected_outputs.

### Implementation for User Story 3

- [ ] T012 [US3] Verify YAML frontmatter of all 7 templates parses cleanly with Python's yaml module
- [ ] T013 [US3] Ensure `expected_outputs` lists are complete and `required` flags are correct

**Checkpoint**: `adm check` (future) can validate phase completeness from templates alone.

---

## Phase 6: Polish & Cross-Cutting

**Purpose**: Final consistency pass

- [ ] T014 Verify cross-references between templates (each template's `depends_on` matches the prior template's `expected_outputs`)
- [ ] T015 Verify templates are self-contained and readable without prior ADM knowledge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Create reference template first
- **US1 (Phase 3)**: All 6 remaining templates — parallelizable after T003
- **US2 (Phase 4)**: Enhancement pass — depends on all templates existing
- **US3 (Phase 5)**: Validation pass — depends on US2 completion
- **Polish (Phase 6)**: Final check — depends on all above

### Parallel Opportunities

```
T004, T005, T006, T007, T008, T009 — all [P], can run simultaneously
```

---

## Implementation Strategy

### MVP (User Story 1 only)

1. T001-T002: Setup
2. T003: Reference template (lineage)
3. T004-T009: Remaining 6 templates in parallel
4. **STOP and VALIDATE**: All 7 files exist with valid frontmatter

### Full Delivery

1. MVP above
2. T010-T011: Agent-readability enhancement
3. T012-T013: Frontmatter validation
4. T014-T015: Polish

---

## Summary

- **Total tasks**: 15
- **Parallel tasks**: 6 (T004-T009)
- **MVP scope**: T001-T009 (9 tasks)
- **Estimated effort**: S (1-2 days)
