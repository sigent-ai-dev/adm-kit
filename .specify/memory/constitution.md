# ADM Kit Constitution

## Core Principles

### I. Discover, Don't Prescribe

Data schemas are hypotheses about reality, not requirements to implement. Every phase produces evidence; only validated evidence becomes a contract.

### II. Phase Gates Are Hard

No skipping phases. Each builds on the previous. The state file is the single source of truth for domain progression.

### III. Preserve Analyst Work

Resolutions to clarification questions survive re-runs. The system never silently discards human decisions.

### IV. Falsify Before Ratcheting

A thesis is a claim. Validation attempts to break it. Only unfalsified, stable theses become contracts.

### V. Immutable Contracts

Once ratcheted, a contract version is frozen. Changes require a new semver version. No editing in place.

### VI. Templates Over Code

The intelligence lives in command markdown (consumed by AI agents), not in Python. The CLI is thin state management.

## Quality Standards

- Every column must be inventoried (Phase 2 completeness)
- Every invariant must be runnable as a pytest (Phase 3 executability)
- Thesis models must use Pydantic with full type annotations (Phase 4 type safety)
- Validation must run against real data, not synthetic fixtures (Phase 5 reality)
- Ratcheting requires zero PENDING invariants (Phase 6 stability)

## Development Workflow

- Use Spec Kit commands (`/speckit-specify`, `/speckit-plan`, `/speckit-implement`) to develop features
- Run `/speckit-selfreview` before requesting PR review
- Use `/speckit-decompose` to break design work into issues
- CLI uses Python 3.11+, typer, rich, Pydantic v2
- Distributed via `uv tool install`

## Governance

Constitution supersedes all other practices. Amendments require documentation and a new version.

**Version**: 1.0.0 | **Ratified**: 2026-05-20
