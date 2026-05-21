"""Clarify-gate pattern — structured CLR-NNN questions that persist across re-runs."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from .schema import ProjectState, ResolutionStatus, save_state


class MergeMode(str, Enum):
    MERGE = "merge"
    OVERWRITE = "overwrite"
    SKIP = "skip"


def next_clr_id(domain: str, state: ProjectState) -> str:
    """Compute the next available CLR-NNN ID for a domain."""
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    existing = state.domains[domain].resolutions
    if not existing:
        return "CLR-001"

    max_num = 0
    for key in existing:
        if key.startswith("CLR-") and key[4:].isdigit():
            max_num = max(max_num, int(key[4:]))
    return f"CLR-{max_num + 1:03d}"


def raise_clr(
    domain: str,
    state: ProjectState,
    state_path: Path,
) -> str:
    """Raise a new open clarification and return the assigned CLR-NNN ID.

    The question text and context are stored in artefact files by the
    calling phase command, not in the state file.
    """
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    clr_id = next_clr_id(domain, state)
    state.domains[domain].resolutions[clr_id] = ResolutionStatus.OPEN
    save_state(state, state_path)
    return clr_id


def resolve_clr(
    domain: str,
    clr_id: str,
    state: ProjectState,
    state_path: Path,
) -> None:
    """Mark a CLR as resolved."""
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    resolutions = state.domains[domain].resolutions
    if clr_id not in resolutions:
        raise ValueError(f"CLR '{clr_id}' does not exist in domain '{domain}'")

    resolutions[clr_id] = ResolutionStatus.RESOLVED
    save_state(state, state_path)


def merge_clarifications(
    domain: str,
    new_clr_ids: list[str],
    state: ProjectState,
    state_path: Path,
    mode: MergeMode = MergeMode.MERGE,
) -> None:
    """Apply merge behaviour when a phase is re-run with new CLRs.

    - merge: preserve existing resolutions, add new as open
    - overwrite: discard all prior resolutions, all new are open
    - skip: don't add any new CLRs, keep existing only
    """
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    resolutions = state.domains[domain].resolutions

    if mode == MergeMode.OVERWRITE:
        resolutions.clear()
        for clr_id in new_clr_ids:
            resolutions[clr_id] = ResolutionStatus.OPEN

    elif mode == MergeMode.SKIP:
        pass  # No changes — existing resolutions stay, no new ones added

    elif mode == MergeMode.MERGE:
        for clr_id in new_clr_ids:
            if clr_id not in resolutions:
                resolutions[clr_id] = ResolutionStatus.OPEN
            # If already exists (resolved or open), leave as-is

    save_state(state, state_path)


def get_clr_summary(domain: str, state: ProjectState) -> tuple[int, int]:
    """Return (open_count, resolved_count) for a domain."""
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    resolutions = state.domains[domain].resolutions
    open_count = sum(1 for s in resolutions.values() if s == ResolutionStatus.OPEN)
    resolved_count = sum(1 for s in resolutions.values() if s == ResolutionStatus.RESOLVED)
    return open_count, resolved_count
