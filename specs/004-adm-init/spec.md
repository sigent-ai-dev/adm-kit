# Feature Specification: Implement `adm init`

**Feature Branch**: `feature/4-adm-init`

**Created**: 2026-05-20

**Status**: Draft

**Input**: Implement the `adm init <domain>` CLI command that bootstraps a domain for ADM analysis — creates the state file, artefact directories, and installs phase templates and command files.

## User Scenarios & Testing

### User Story 1 - Developer initialises a new domain (Priority: P1)

A developer has source data (e.g., `holdings.csv`) and wants to start the ADM process. They run `adm init holdings --source ./data/holdings.csv` and get a fully scaffolded domain ready for Phase 1.

**Why this priority**: This is the entry point for all ADM work. Without a working `init`, nothing else functions.

**Independent Test**: Run `adm init holdings --source ./data/test.csv` in an empty directory and verify the complete directory structure is created.

**Acceptance Scenarios**:

1. **Given** an empty project directory, **When** `adm init holdings --source ./data/file.csv` runs, **Then** `.adm/project.json` is created with domain entry at phase 1.
2. **Given** the init command completes, **When** checking the filesystem, **Then** `artefacts/holdings/` contains directories `1-lineage/` through `7-model/`.
3. **Given** the `--ai claude` flag, **When** init runs, **Then** command files are installed to `.claude/commands/` with `adm.` prefix.

---

### User Story 2 - Developer adds a second domain to existing project (Priority: P1)

A developer has already initialised `holdings` and now wants to add `cashflows` as a second domain. Running `adm init cashflows` adds to the existing state file without disturbing the first domain.

**Why this priority**: Multi-domain support is a core ADM capability. Init must be additive, not destructive.

**Independent Test**: Init two domains sequentially, verify both exist in state file and have independent artefact trees.

**Acceptance Scenarios**:

1. **Given** a project with `holdings` domain, **When** `adm init cashflows` runs, **Then** both domains appear in `.adm/project.json`.
2. **Given** an existing domain, **When** `adm init holdings` runs without `--force`, **Then** the command refuses with "domain already exists" error.
3. **Given** an existing domain, **When** `adm init holdings --force` runs, **Then** the domain is re-initialised (reset to phase 1).

---

### User Story 3 - Developer chooses which AI agent to install for (Priority: P2)

A developer using Gemini instead of Claude runs `adm init holdings --ai gemini` and gets command files installed in `.gemini/commands/` instead of `.claude/commands/`.

**Why this priority**: Multi-agent support is a stated goal, but the scaffolding must work for at least one agent first.

**Independent Test**: Run init with different `--ai` flags and verify commands land in the correct agent directory.

**Acceptance Scenarios**:

1. **Given** `--ai claude`, **When** init runs, **Then** commands are installed to `.claude/commands/`.
2. **Given** `--ai gemini`, **When** init runs, **Then** commands are installed to `.gemini/commands/`.
3. **Given** no `--ai` flag, **When** init runs, **Then** defaults to claude.

---

### Edge Cases

- What if `.adm/project.json` exists but is corrupt/invalid? Init should detect and offer to recreate.
- What if the source file doesn't exist? Warn but don't block — source can be provided later.
- What if the artefact directory already has content (partial previous run)? Respect existing files unless `--force`.

## Requirements

### Functional Requirements

- **FR-001**: `adm init <domain>` MUST create `.adm/project.json` if it doesn't exist
- **FR-002**: `adm init <domain>` MUST add a domain entry with `current_phase: 1, iteration: 1, contract_version: null, resolutions: {}`
- **FR-003**: `adm init <domain>` MUST create `artefacts/<domain>/` with subdirectories for all 7 phases
- **FR-004**: `adm init <domain>` MUST install command files to the appropriate AI agent directory
- **FR-005**: `adm init <domain>` MUST refuse to re-init an existing domain without `--force`
- **FR-006**: `adm init <domain> --source <path>` MUST record the source path in the domain state
- **FR-007**: `adm init <domain> --ai <agent>` MUST support at minimum: claude, gemini, copilot, cursor, q, windsurf
- **FR-008**: `adm init` MUST display a success summary showing what was created
- **FR-009**: Multi-domain MUST be additive — init of a new domain preserves existing domains

### Key Entities

- **Domain**: A named data domain being modelled (e.g., "holdings", "cashflows")
- **State File**: `.adm/project.json` — tracks all domains and their phase progression
- **Artefact Tree**: `artefacts/<domain>/<N>-<phase>/` — directory structure for phase outputs
- **Agent Directory**: The target directory for command file installation (varies by AI agent)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Running `adm init holdings` in an empty directory creates a valid project in under 2 seconds
- **SC-002**: The created `.adm/project.json` validates against the Pydantic state schema
- **SC-003**: All 7 artefact subdirectories exist after init
- **SC-004**: Command files are installed and readable in the correct agent directory

## Clarifications

### Session 2026-05-20

- Q: How should `adm init` access template files at runtime (CLI is distributed via `uv tool install`)? → A: Bundle templates inside the Python package using `importlib.resources`. Always available after install.

## Assumptions

- The state schema from issue #1 is available (`src/adm_cli/schema.py`)
- Phase templates from issue #2 are available in `templates/phases/`
- Command files from issue #3 are available in `templates/commands/`
- The CLI framework is typer + rich (already in pyproject.toml)
- Source file existence is validated with a warning, not an error (analyst may add it later)
