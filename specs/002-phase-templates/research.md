# Research: Phase Artefact Templates

## Decision: Template frontmatter format

**Decision**: YAML frontmatter (fenced by `---`) at the top of each markdown template file.

**Rationale**: YAML frontmatter is a well-established convention in static site generators, Hugo, Jekyll, and Spec Kit itself. Python's `yaml` module (stdlib-adjacent via PyYAML, already common) can parse it trivially. It keeps the template self-contained — one file per phase.

**Alternatives considered**:
- Separate `manifest.json` per phase — rejected because it splits the template across two files, increasing maintenance burden and drift risk
- Markdown table parsing — rejected because it's fragile and requires custom parsing logic

## Decision: Versioned directory handling in templates

**Decision**: Templates for phases 4 (thesis) and 5 (validate) set `versioned: true` in frontmatter. The expected_outputs list describes files relative to a version subdirectory. Phase 6 (ratchet) uses semver directories (e.g., `v1.0.0/`) — indicated by a `versioning: semver` field.

**Rationale**: The ADM methodology requires iteration on thesis and validation. Versioned directories allow multiple attempts without overwriting prior work. Ratcheted contracts use semver because they're immutable releases.

**Alternatives considered**:
- Flat files with version suffixes (e.g., `thesis-v1.md`) — rejected because it clutters the directory and makes cleanup harder
- Single file overwritten each iteration — rejected because it violates "preserve analyst work" principle

## Decision: Completion criteria format

**Decision**: Each template includes a `## Completion Criteria` section with a bulleted list of testable conditions. `adm check` will parse the `expected_outputs` frontmatter for file existence, and the completion criteria for human/agent judgment.

**Rationale**: File existence is machine-checkable (frontmatter). Content quality requires judgment (completion criteria in prose). Separating these concerns keeps both reliable.
