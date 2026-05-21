"""Tests for `adm status` command."""

from pathlib import Path

import pytest

from adm_cli.schema import DomainState, ProjectState, ResolutionStatus, save_state
from adm_cli.status import run_status


class TestStatusDisplay:
    def test_shows_single_domain(self, tmp_path: Path):
        state = ProjectState(
            domains={"holdings": DomainState(current_phase=4, iteration=2)}
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        run_status(project_dir=tmp_path)

    def test_shows_multiple_domains(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(current_phase=4, iteration=2),
                "cashflows": DomainState(current_phase=7, contract_version="1.0.0"),
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        run_status(project_dir=tmp_path)

    def test_shows_open_questions_count(self, tmp_path: Path):
        state = ProjectState(
            domains={
                "holdings": DomainState(
                    current_phase=3,
                    resolutions={
                        "CLR-001": ResolutionStatus.OPEN,
                        "CLR-002": ResolutionStatus.OPEN,
                        "CLR-003": ResolutionStatus.RESOLVED,
                    },
                )
            }
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        run_status(project_dir=tmp_path)

    def test_contract_version_displayed(self, tmp_path: Path):
        state = ProjectState(
            domains={"holdings": DomainState(current_phase=7, contract_version="2.1.0")}
        )
        save_state(state, tmp_path / ".adm" / "project.json")
        run_status(project_dir=tmp_path)


class TestStatusEdgeCases:
    def test_no_state_file(self, tmp_path: Path):
        with pytest.raises(SystemExit) as exc_info:
            run_status(project_dir=tmp_path)
        assert exc_info.value.code == 1

    def test_empty_project(self, tmp_path: Path):
        state = ProjectState()
        save_state(state, tmp_path / ".adm" / "project.json")
        run_status(project_dir=tmp_path)
