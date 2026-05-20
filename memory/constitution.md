# ADM Kit Constitution

## Core Principles

1. **Discover, don't prescribe** — data schemas are hypotheses about reality, not requirements to implement. They must be validated against real snapshots.
2. **Falsify before ratcheting** — a thesis is a claim. Validation attempts to break it. Only unfalsified, stable theses become contracts.
3. **Preserve analyst work** — resolutions to clarification questions survive re-runs. The system never silently discards human decisions.
4. **Phase gates are hard** — no skipping phases. Each builds on the previous. The state file is the single source of truth.
5. **Immutable contracts** — once ratcheted, a contract version is frozen. Changes require a new semver version.
6. **Audit everything** — every phase completion, every clarification resolution, every ratchet decision.

## Quality Standards

- Every column must be inventoried (Phase 2 completeness)
- Every invariant must be runnable as a pytest (Phase 3 executability)
- Thesis models must use Pydantic with full type annotations (Phase 4 type safety)
- Validation must run against real data, not synthetic fixtures (Phase 5 reality)
- Ratcheting requires zero PENDING invariants (Phase 6 stability)

## Integration Contract

- ADM contracts hand off to Spec Kit via `/adm.model` (Phase 7)
- The handoff produces a `feature.json` + `spec.md` seed
- Contract field names become entity definitions in the spec
- Invariants become acceptance criteria seeds
