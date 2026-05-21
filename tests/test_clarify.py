"""Tests for clarify-gate pattern."""

from pathlib import Path

import pytest

from adm_cli.clarify import (
    MergeMode,
    get_clr_summary,
    merge_clarifications,
    next_clr_id,
    raise_clr,
    resolve_clr,
)
from adm_cli.schema import DomainState, ProjectState, ResolutionStatus, save_state


def _setup(tmp_path: Path, **kwargs) -> tuple[ProjectState, Path]:
    state = ProjectState(domains={"holdings": DomainState(**kwargs)})
    state_path = tmp_path / ".adm" / "project.json"
    save_state(state, state_path)
    return state, state_path


class TestNextClrId:
    def test_first_id(self, tmp_path: Path):
        state, _ = _setup(tmp_path)
        assert next_clr_id("holdings", state) == "CLR-001"

    def test_sequential(self, tmp_path: Path):
        state, _ = _setup(tmp_path, resolutions={"CLR-001": ResolutionStatus.OPEN})
        assert next_clr_id("holdings", state) == "CLR-002"

    def test_gaps_use_max(self, tmp_path: Path):
        state, _ = _setup(
            tmp_path,
            resolutions={"CLR-001": ResolutionStatus.RESOLVED, "CLR-005": ResolutionStatus.OPEN},
        )
        assert next_clr_id("holdings", state) == "CLR-006"

    def test_nonexistent_domain(self, tmp_path: Path):
        state, _ = _setup(tmp_path)
        with pytest.raises(ValueError, match="does not exist"):
            next_clr_id("nonexistent", state)


class TestRaiseClr:
    def test_raises_open(self, tmp_path: Path):
        state, state_path = _setup(tmp_path)
        clr_id = raise_clr("holdings", state, state_path)
        assert clr_id == "CLR-001"
        assert state.domains["holdings"].resolutions["CLR-001"] == ResolutionStatus.OPEN

    def test_sequential_ids(self, tmp_path: Path):
        state, state_path = _setup(tmp_path)
        id1 = raise_clr("holdings", state, state_path)
        id2 = raise_clr("holdings", state, state_path)
        assert id1 == "CLR-001"
        assert id2 == "CLR-002"

    def test_persists_to_disk(self, tmp_path: Path):
        from adm_cli.schema import load_state

        state, state_path = _setup(tmp_path)
        raise_clr("holdings", state, state_path)
        reloaded = load_state(state_path)
        assert "CLR-001" in reloaded.domains["holdings"].resolutions


class TestResolveClr:
    def test_marks_resolved(self, tmp_path: Path):
        state, state_path = _setup(tmp_path, resolutions={"CLR-001": ResolutionStatus.OPEN})
        resolve_clr("holdings", "CLR-001", state, state_path)
        assert state.domains["holdings"].resolutions["CLR-001"] == ResolutionStatus.RESOLVED

    def test_nonexistent_clr(self, tmp_path: Path):
        state, state_path = _setup(tmp_path)
        with pytest.raises(ValueError, match="does not exist"):
            resolve_clr("holdings", "CLR-999", state, state_path)


class TestMergeClarifications:
    def test_merge_preserves_existing(self, tmp_path: Path):
        state, state_path = _setup(
            tmp_path,
            resolutions={"CLR-001": ResolutionStatus.RESOLVED},
        )
        merge_clarifications("holdings", ["CLR-001", "CLR-002"], state, state_path, MergeMode.MERGE)
        assert state.domains["holdings"].resolutions["CLR-001"] == ResolutionStatus.RESOLVED
        assert state.domains["holdings"].resolutions["CLR-002"] == ResolutionStatus.OPEN

    def test_overwrite_discards_all(self, tmp_path: Path):
        state, state_path = _setup(
            tmp_path,
            resolutions={"CLR-001": ResolutionStatus.RESOLVED, "CLR-002": ResolutionStatus.RESOLVED},
        )
        merge_clarifications("holdings", ["CLR-001", "CLR-003"], state, state_path, MergeMode.OVERWRITE)
        resolutions = state.domains["holdings"].resolutions
        assert resolutions == {"CLR-001": ResolutionStatus.OPEN, "CLR-003": ResolutionStatus.OPEN}

    def test_skip_adds_nothing(self, tmp_path: Path):
        state, state_path = _setup(
            tmp_path,
            resolutions={"CLR-001": ResolutionStatus.RESOLVED},
        )
        merge_clarifications("holdings", ["CLR-002", "CLR-003"], state, state_path, MergeMode.SKIP)
        assert "CLR-002" not in state.domains["holdings"].resolutions
        assert state.domains["holdings"].resolutions["CLR-001"] == ResolutionStatus.RESOLVED


class TestGetClrSummary:
    def test_counts(self, tmp_path: Path):
        state, _ = _setup(
            tmp_path,
            resolutions={
                "CLR-001": ResolutionStatus.OPEN,
                "CLR-002": ResolutionStatus.OPEN,
                "CLR-003": ResolutionStatus.RESOLVED,
            },
        )
        open_count, resolved_count = get_clr_summary("holdings", state)
        assert open_count == 2
        assert resolved_count == 1

    def test_empty(self, tmp_path: Path):
        state, _ = _setup(tmp_path)
        open_count, resolved_count = get_clr_summary("holdings", state)
        assert open_count == 0
        assert resolved_count == 0
