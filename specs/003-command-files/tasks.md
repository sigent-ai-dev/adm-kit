# Tasks: AI Agent Command Files

**Input**: Design documents from `specs/003-command-files/`

**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: Not requested — template-only feature.

## Phase 1: Setup

**Purpose**: Establish the standard and fix the namespace issue

- [ ] T001 Update `templates/commands/lineage.md` — replace all `OQ-NNN` references with `CLR-NNN`

---

## Phase 2: Foundational

**Purpose**: Create the new clarify command (blocks nothing but completes the set)

- [ ] T002 Create `templates/commands/clarify.md` — utility command for resolving CLR-NNN questions at any phase

---

## Phase 3: User Story 1 — Agent executes phases end-to-end (Priority: P1)

**Goal**: All 7 phase commands have complete gate checks, execution flows, output structures, and guidelines.

**Independent Test**: Verify each command file has frontmatter, gate check, execution flow, output structure, and guidelines sections.

### Implementation for User Story 1

- [ ] T003 [P] [US1] Review and complete `templates/commands/inventory.md` — ensure gate check references `lineage.md`+`lineage.json`, outputs match phase template
- [ ] T004 [P] [US1] Review and complete `templates/commands/invariants.md` — ensure gate check references inventory artefacts, outputs match phase template
- [ ] T005 [P] [US1] Review and complete `templates/commands/thesis.md` — ensure iteration versioning (v1/, v2/) is documented in execution flow
- [ ] T006 [P] [US1] Review and complete `templates/commands/validate.md` — ensure iteration versioning and falsification process are documented
- [ ] T007 [P] [US1] Review and complete `templates/commands/ratchet.md` — ensure zero-PENDING-invariants gate is explicit, semver logic documented
- [ ] T008 [P] [US1] Review and complete `templates/commands/model.md` — ensure Spec Kit handoff (feature.json + spec.md) is clearly documented

**Checkpoint**: All 8 command files (7 phases + clarify) are complete and structurally consistent.

---

## Phase 4: User Story 3 — Gate enforcement (Priority: P1)

**Goal**: Gate checks in each command correctly reference prior phase artefacts from phase templates.

### Implementation for User Story 3

- [ ] T009 [US3] Cross-reference all gate checks against phase template `depends_on.artefacts` — fix any mismatches

**Checkpoint**: Gate checks are provably correct against phase template definitions.

---

## Phase 5: Polish & Cross-Cutting

- [ ] T010 Verify all command files use consistent terminology (CLR-NNN, not OQ-NNN)
- [ ] T011 Verify all handoffs sections point to the correct next command

---

## Dependencies & Execution Order

- **T001**: First (namespace fix)
- **T002**: Independent (new file)
- **T003-T008**: All parallel after T001
- **T009**: After T003-T008 (needs complete commands to cross-reference)
- **T010-T011**: After T009 (final validation)

## Summary

- **Total tasks**: 11
- **Parallel tasks**: 6 (T003-T008)
- **MVP scope**: T001-T008 (8 tasks)
- **Estimated effort**: S (1-2 days)
