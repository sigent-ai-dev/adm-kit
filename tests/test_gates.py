"""Tests for phase gate enforcement."""

from pathlib import Path

import pytest

from adm_cli.gates import advance_phase, can_advance
from adm_cli.constants import PHASE_DIRS
from adm_cli.schema import DomainState, ProjectState, ResolutionStatus, save_state


def _setup_project(tmp_path: Path, phase: int = 1, **kwargs) -> ProjectState:
    """Create a project with a domain at the given phase."""
    state = ProjectState(domains={"holdings": DomainState(current_phase=phase, **kwargs)})
    save_state(state, tmp_path / ".adm" / "project.json")
    return state


def _create_phase_artefacts(tmp_path: Path, domain: str, phase: int) -> None:
    """Create required artefact files for a phase based on template expectations."""
    phase_dir = tmp_path / "artefacts" / domain / PHASE_DIRS[phase - 1]
    phase_dir.mkdir(parents=True, exist_ok=True)
    # Create the minimum required files per phase
    files_by_phase = {
        1: ["lineage.md", "lineage.json"],
        2: ["inventory.md", "inventory.json"],
        3: ["invariants.md", "invariants.py", "invariants.json"],
        4: ["thesis.md", "draft.py", "draft.schema.json"],
        5: ["report.md", "report.json"],
        6: ["contract.py", "contract.schema.json"],
        7: ["feature.json", "spec.md"],
    }
    for filename in files_by_phase.get(phase, []):
        (phase_dir / filename).write_text(f"# placeholder for {filename}\n")


class TestCanAdvance:
    def test_allows_when_artefacts_present(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=1)
        _create_phase_artefacts(tmp_path, "holdings", 1)
        allowed, reason = can_advance("holdings", 2, state, tmp_path)
        assert allowed is True

    def test_blocks_when_artefacts_missing(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=1)
        # Don't create artefacts
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[0]).mkdir(parents=True)
        allowed, reason = can_advance("holdings", 2, state, tmp_path)
        assert allowed is False
        assert "Missing required artefacts" in reason

    def test_blocks_when_directory_missing(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=1)
        allowed, reason = can_advance("holdings", 2, state, tmp_path)
        assert allowed is False
        assert "missing" in reason.lower()

    def test_blocks_phase_skipping(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=2)
        allowed, reason = can_advance("holdings", 5, state, tmp_path)
        assert allowed is False
        assert "no skipping" in reason.lower()

    def test_blocks_beyond_phase_7(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=7)
        allowed, reason = can_advance("holdings", 8, state, tmp_path)
        assert allowed is False
        assert "beyond phase 7" in reason.lower()

    def test_blocks_nonexistent_domain(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=1)
        allowed, reason = can_advance("nonexistent", 2, state, tmp_path)
        assert allowed is False
        assert "does not exist" in reason

    def test_ratchet_gate_blocks_on_open_clrs(self, tmp_path: Path):
        state = _setup_project(
            tmp_path,
            phase=5,
            resolutions={"CLR-001": ResolutionStatus.OPEN, "CLR-002": ResolutionStatus.RESOLVED},
        )
        _create_phase_artefacts(tmp_path, "holdings", 5)
        allowed, reason = can_advance("holdings", 6, state, tmp_path)
        assert allowed is False
        assert "open clarifications" in reason.lower()

    def test_ratchet_gate_passes_when_all_resolved(self, tmp_path: Path):
        state = _setup_project(
            tmp_path,
            phase=5,
            resolutions={"CLR-001": ResolutionStatus.RESOLVED, "CLR-002": ResolutionStatus.RESOLVED},
        )
        _create_phase_artefacts(tmp_path, "holdings", 5)
        allowed, reason = can_advance("holdings", 6, state, tmp_path)
        assert allowed is True

    def test_stability_window_blocks_when_too_recent(self, tmp_path: Path):
        from datetime import date

        state = _setup_project(
            tmp_path,
            phase=5,
            stability_window_days=7,
            last_thesis_change=date.today().isoformat(),
        )
        _create_phase_artefacts(tmp_path, "holdings", 5)
        allowed, reason = can_advance("holdings", 6, state, tmp_path)
        assert allowed is False
        assert "stability window" in reason.lower()

    def test_stability_window_passes_when_elapsed(self, tmp_path: Path):
        from datetime import date, timedelta

        past = (date.today() - timedelta(days=10)).isoformat()
        state = _setup_project(
            tmp_path,
            phase=5,
            stability_window_days=7,
            last_thesis_change=past,
        )
        _create_phase_artefacts(tmp_path, "holdings", 5)
        allowed, reason = can_advance("holdings", 6, state, tmp_path)
        assert allowed is True

    def test_stability_window_zero_allows_immediate(self, tmp_path: Path):
        from datetime import date

        state = _setup_project(
            tmp_path,
            phase=5,
            stability_window_days=0,
            last_thesis_change=date.today().isoformat(),
        )
        _create_phase_artefacts(tmp_path, "holdings", 5)
        allowed, reason = can_advance("holdings", 6, state, tmp_path)
        assert allowed is True


class TestAdvancePhase:
    def test_increments_phase(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=3)
        state_path = tmp_path / ".adm" / "project.json"
        advance_phase("holdings", state, state_path)
        assert state.domains["holdings"].current_phase == 4

    def test_saves_state(self, tmp_path: Path):
        from adm_cli.schema import load_state

        state = _setup_project(tmp_path, phase=2)
        state_path = tmp_path / ".adm" / "project.json"
        advance_phase("holdings", state, state_path)
        reloaded = load_state(state_path)
        assert reloaded.domains["holdings"].current_phase == 3

    def test_rejects_at_phase_7(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=7)
        state_path = tmp_path / ".adm" / "project.json"
        with pytest.raises(ValueError, match="already at phase 7"):
            advance_phase("holdings", state, state_path)

    def test_rejects_nonexistent_domain(self, tmp_path: Path):
        state = _setup_project(tmp_path, phase=1)
        state_path = tmp_path / ".adm" / "project.json"
        with pytest.raises(ValueError, match="does not exist"):
            advance_phase("nonexistent", state, state_path)
