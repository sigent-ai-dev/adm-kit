# Feature Specification: AI Agent Command Files

**Feature Branch**: `feature/3-command-files`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Complete the AI agent command files for all 7 ADM phases plus the /adm.clarify utility command. Each command file is a markdown document consumed by AI agents (Claude, Gemini, Copilot, etc.) that instructs the agent how to execute a specific ADM phase — what to read, what to produce, what gates to check.

## User Scenarios & Testing

### User Story 1 - AI agent executes a phase command end-to-end (Priority: P1)

A developer types `/adm.lineage` in their AI assistant. The agent reads the command file, understands the phase inputs/outputs/process, and produces conformant artefacts in the correct directory structure without additional guidance.

**Why this priority**: Command files are the primary interface between developers and ADM Kit. Without complete, actionable instructions, agents cannot execute phases correctly.

**Independent Test**: An AI agent given only the command file + source data produces artefacts that match the phase template's expected_outputs specification.

**Acceptance Scenarios**:

1. **Given** a command file with frontmatter and execution flow, **When** an AI agent reads it, **Then** it knows what inputs to read, what to produce, and where to write outputs.
2. **Given** an incomplete prior phase, **When** the agent reads the command file's gate check, **Then** it refuses to proceed and explains what's missing.
3. **Given** a completed prior phase, **When** the agent executes the command, **Then** it produces all expected_outputs listed in the corresponding phase template.

---

### User Story 2 - Developer understands what a command does before running it (Priority: P2)

A developer opens a command file to understand what `/adm.invariants` will do before invoking it. The file serves as both agent instructions AND human documentation.

**Why this priority**: Transparency builds trust. Developers need to audit what the AI will do.

**Independent Test**: A developer unfamiliar with ADM can read a command file and explain what it does to a colleague.

**Acceptance Scenarios**:

1. **Given** any command file, **When** a developer reads it, **Then** they understand the purpose, inputs, outputs, and process without referencing other files.
2. **Given** the `/adm.clarify` command, **When** a developer reads it, **Then** they understand it can be run at any phase to resolve open questions.

---

### User Story 3 - Commands enforce phase gate discipline (Priority: P1)

Each command file includes a gate check section that refuses to execute if prerequisites aren't met. This enforces the ADM principle that phases cannot be skipped.

**Why this priority**: Phase gates are a core ADM principle. Without enforcement in command files, agents would happily skip phases.

**Independent Test**: Invoke a phase command when its prerequisite phase is incomplete and verify the agent refuses.

**Acceptance Scenarios**:

1. **Given** Phase 2 has not completed (no `inventory.md`), **When** `/adm.invariants` is invoked, **Then** the command instructs the agent to refuse and report what's missing.
2. **Given** all prior phases are complete, **When** any phase command is invoked, **Then** the gate check passes silently and execution proceeds.

---

### Edge Cases

- What happens if the domain has open CLR-NNN questions? Commands should note them but not block (only ratchet blocks on PENDING invariants).
- How do thesis/validate handle iteration (v1 → v2)? Commands must instruct agents on version directory creation.
- What if source data changes between phases? Commands should instruct agents to note discrepancies.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a command file for each of the 7 phases: lineage, inventory, invariants, thesis, validate, ratchet, model
- **FR-002**: System MUST provide a `/adm.clarify` utility command usable at any phase
- **FR-003**: Each command file MUST include frontmatter with `description` field
- **FR-004**: Each command file MUST include a gate check section that validates prerequisites before execution
- **FR-005**: Each command file MUST specify: inputs (what to read), outputs (what to produce and where), execution flow (step-by-step process)
- **FR-006**: Commands MUST reference the phase template's expected_outputs for output conformance
- **FR-007**: Commands for phases 4 (thesis) and 5 (validate) MUST handle iteration versioning (v1/, v2/)
- **FR-008**: The ratchet command (phase 6) MUST enforce zero-PENDING-invariants gate

### Key Entities

- **Command File**: A markdown document in `templates/commands/` that instructs AI agents how to execute one ADM phase
- **Gate Check**: A prerequisites section that validates prior phase completion before allowing execution
- **Execution Flow**: Numbered steps the agent follows to produce artefacts

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 8 command files exist (7 phases + clarify) with complete frontmatter
- **SC-002**: Each command file contains gate check, inputs, outputs, and execution flow sections
- **SC-003**: An AI agent following any command file produces output matching the phase template's expected_outputs
- **SC-004**: Gate checks correctly reference prior phase artefacts (traceability to phase templates)

## Clarifications

### Session 2026-05-20

- Q: Standardise open question IDs — `OQ-NNN` (in existing commands) vs `CLR-NNN` (in state schema)? → A: Standardise on `CLR-NNN` everywhere. Update existing `OQ-NNN` references in command files to `CLR-NNN`.

## Assumptions

- Command files are stored in `templates/commands/` and installed into projects on `adm init`
- 7 command files already exist but need completion (currently partial/placeholder)
- The clarify command (`/adm.clarify`) is new and needs to be created
- Command files are consumed by AI agents via slash-command patterns (e.g., `/adm.lineage`)
- The same command file works across all supported AI agents (format is agent-agnostic markdown)
