# Feature Specification: Phase Artefact Templates

**Feature Branch**: `feature/2-phase-templates`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Create phase artefact templates for all 7 ADM phases. Each template defines the expected structure, format, and content for artefacts produced during that phase, following the `artefacts/<domain>/<N>-<phase>/` layout convention.

## User Scenarios & Testing

### User Story 1 - Developer initialises a domain and sees phase scaffolding (Priority: P1)

A developer runs `adm init holdings` and the tool creates the artefact directory structure with template files for each phase, giving them a clear starting point for each phase's expected outputs.

**Why this priority**: Without templates, developers have no guidance on what each phase should produce. This is the minimum viable scaffolding.

**Independent Test**: Can be tested by running `adm init` and verifying all 7 phase directories contain the expected template files with correct structure.

**Acceptance Scenarios**:

1. **Given** a fresh project, **When** `adm init holdings` runs, **Then** `artefacts/holdings/` contains directories `1-lineage/` through `7-model/` each with a template file.
2. **Given** an initialised domain, **When** a developer opens a phase template, **Then** it documents expected inputs, outputs, artefact format, and validation criteria for that phase.

---

### User Story 2 - AI agent consumes template to know what to produce (Priority: P1)

An AI agent (Claude, Gemini, etc.) executing a phase command reads the phase template to understand what artefact format and content is expected, ensuring consistent output across different agents and runs.

**Why this priority**: Templates are the contract between the command instructions and the artefact output. Without them, agents produce inconsistent formats.

**Independent Test**: An AI agent given only the template and source data can produce a conformant artefact without additional guidance.

**Acceptance Scenarios**:

1. **Given** a lineage template, **When** an AI agent reads it, **Then** it knows to produce `lineage.md` and `lineage.json` with specified sections and schema.
2. **Given** a thesis template, **When** the agent reads it, **Then** it knows to produce versioned subdirectories (`v1/`, `v2/`) containing `thesis.md`, `draft.py`, and `draft.schema.json`.

---

### User Story 3 - Developer validates artefact completeness against template (Priority: P2)

A developer or the `adm check` command compares actual artefacts against the template to determine if a phase is complete enough to advance through the gate.

**Why this priority**: Phase gates depend on knowing "what complete looks like" — that's defined by the template.

**Independent Test**: `adm check` can read a template and report which expected files/sections are present vs missing.

**Acceptance Scenarios**:

1. **Given** a completed lineage phase with all template-specified files, **When** `adm check` runs, **Then** it reports the phase as complete.
2. **Given** a partially completed inventory phase (missing `inventory.json`), **When** `adm check` runs, **Then** it reports the missing artefact and blocks gate advancement.

---

### Edge Cases

- What happens when a phase template references optional sections that don't apply to all domains?
- How does the system handle thesis/validation versioned subdirectories (v1/, v2/) in the template?
- What if a developer modifies a template after initialisation — does the system detect drift?

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a template file for each of the 7 ADM phases (lineage, inventory, invariants, thesis, validate, ratchet, model)
- **FR-002**: Each template MUST document: expected inputs, expected outputs (file names and formats), artefact structure, and completion criteria
- **FR-003**: Templates MUST follow the `artefacts/<domain>/<N>-<phase>/` directory convention
- **FR-004**: Thesis (phase 4) and validation (phase 5) templates MUST document the versioned subdirectory convention (`v1/`, `v2/`, ...)
- **FR-005**: Templates MUST include a YAML frontmatter block listing expected output files so `adm check` can programmatically validate phase completeness
- **FR-006**: Each template MUST reference what inputs from the prior phase it depends on (traceability)
- **FR-007**: Templates MUST be self-contained — readable without prior ADM knowledge

### Key Entities

- **Phase Template**: A markdown file defining the expected artefacts, structure, and completion criteria for one ADM phase
- **Artefact Manifest**: The list of expected output files for a phase (embedded in the template as a structured section)

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 7 phases have a template file in `templates/phases/`
- **SC-002**: Each template contains all mandatory sections (inputs, outputs, structure, completion criteria)
- **SC-003**: A developer unfamiliar with ADM can read any single template and understand what that phase produces
- **SC-004**: `adm check` can parse templates to determine phase completeness (expected files list is extractable)

## Clarifications

### Session 2026-05-20

- Q: How should templates declare expected output files for machine parsing? → A: YAML frontmatter block at top of each template listing expected output files

## Assumptions

- Templates are stored in `templates/phases/` in the ADM Kit source and copied into projects on `adm init`
- Templates are Markdown files consumed by both humans and AI agents
- The template format is stable enough to be a contract for phase gate validation
- Templates define structure, not content — actual domain-specific analysis is done by the AI agent at runtime
