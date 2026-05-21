"""Tests for `adm check` command."""

from pathlib import Path

import pytest

from adm_cli.check import run_check
from adm_cli.constants import PHASE_DIRS
from adm_cli.schema import DomainState, ProjectState, ResolutionStatus, save_state


def _setup_valid_project(tmp_path: Path, phase: int = 3) -> None:
    """Create a valid project at given phase."""
    state = ProjectState(domains={"holdings": DomainState(current_phase=phase)})
    save_state(state, tmp_path / ".adm" / "project.json")
    for i, d in enumerate(PHASE_DIRS, start=1):
        if i > phase:
            break
        (tmp_path / "artefacts" / "holdings" / d).mkdir(parents=True)


class TestValidProject:
    def test_exits_zero(self, tmp_path: Path):
        _setup_valid_project(tmp_path, phase=3)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0

    def test_multi_domain_exits_zero(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(current_phase=2),
                "cashflows": DomainState(current_phase=1),
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        for d in PHASE_DIRS[:2]:
            (tmp_path / "artefacts" / "holdings" / d).mkdir(parents=True)
        (tmp_path / "artefacts" / "cashflows" / PHASE_DIRS[0]).mkdir(parents=True)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0


class TestMissingArtefactDir:
    def test_reports_error_and_exits_nonzero(self, tmp_path: Path):
        state = ProjectState(domains={"holdings": DomainState(current_phase=3)})
        save_state(state, tmp_path / ".adm" / "project.json")
        # Only create dirs for phases 1 and 2, skip phase 3
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[0]).mkdir(parents=True)
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[1]).mkdir(parents=True)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 1


class TestMissingStateFile:
    def test_reports_error(self, tmp_path: Path):
        with pytest.raises(SystemExit) as exc_info:
            run_check(project_dir=tmp_path)
        assert exc_info.value.code == 1


class TestCorruptStateFile:
    def test_reports_schema_error(self, tmp_path: Path):
        state_path = tmp_path / ".adm" / "project.json"
        state_path.parent.mkdir(parents=True)
        state_path.write_text("{invalid json{{}")
        with pytest.raises(SystemExit) as exc_info:
            run_check(project_dir=tmp_path)
        assert exc_info.value.code == 1


class TestClarificationReporting:
    def test_open_clrs_show_warning(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(
                    current_phase=1,
                    resolutions={"CLR-001": ResolutionStatus.OPEN, "CLR-002": ResolutionStatus.RESOLVED},
                )
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[0]).mkdir(parents=True)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0  # warnings don't cause failure

    def test_zero_open_shows_ready(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(
                    current_phase=1,
                    resolutions={"CLR-001": ResolutionStatus.RESOLVED},
                )
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[0]).mkdir(parents=True)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0


class TestInvariantSuite:
    def test_runs_at_phase_4(self, tmp_path: Path):
        _setup_valid_project(tmp_path, phase=4)
        inv_path = tmp_path / "artefacts" / "holdings" / "3-invariants" / "invariants.py"
        inv_path.write_text("def test_always_passes():\n    assert True\n")
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0

    def test_skips_at_phase_2(self, tmp_path: Path):
        _setup_valid_project(tmp_path, phase=2)
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0

    def test_failures_are_warnings(self, tmp_path: Path):
        _setup_valid_project(tmp_path, phase=4)
        inv_path = tmp_path / "artefacts" / "holdings" / "3-invariants" / "invariants.py"
        inv_path.write_text("def test_always_fails():\n    assert False\n")
        exit_code = run_check(project_dir=tmp_path)
        assert exit_code == 0  # warnings don't cause non-zero exit


class TestDomainFilter:
    def test_checks_single_domain(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(current_phase=1),
                "cashflows": DomainState(current_phase=1),
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        (tmp_path / "artefacts" / "holdings" / PHASE_DIRS[0]).mkdir(parents=True)
        # cashflows dir missing — but we only check holdings
        exit_code = run_check(domain_filter="holdings", project_dir=tmp_path)
        assert exit_code == 0

    def test_unknown_domain_exits_nonzero(self, tmp_path: Path):
        _setup_valid_project(tmp_path, phase=1)
        with pytest.raises(SystemExit) as exc_info:
            run_check(domain_filter="nonexistent", project_dir=tmp_path)
        assert exc_info.value.code == 1
