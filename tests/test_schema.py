"""Tests for ADM state schema."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from adm_cli.schema import (
    DomainState,
    ProjectState,
    ResolutionStatus,
    load_state,
    save_state,
)


class TestDomainState:
    def test_defaults(self):
        d = DomainState()
        assert d.current_phase == 1
        assert d.iteration == 1
        assert d.contract_version is None
        assert d.resolutions == {}

    def test_valid_state(self):
        d = DomainState(
            current_phase=4,
            iteration=2,
            contract_version="1.0.0",
            resolutions={"CLR-001": ResolutionStatus.RESOLVED, "CLR-002": ResolutionStatus.OPEN},
        )
        assert d.current_phase == 4
        assert d.iteration == 2
        assert d.contract_version == "1.0.0"
        assert d.resolutions["CLR-001"] == ResolutionStatus.RESOLVED

    def test_phase_too_low(self):
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            DomainState(current_phase=0)

    def test_phase_too_high(self):
        with pytest.raises(ValidationError, match="less than or equal to 7"):
            DomainState(current_phase=8)

    def test_iteration_too_low(self):
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            DomainState(iteration=0)

    def test_invalid_semver(self):
        with pytest.raises(ValidationError, match="semver"):
            DomainState(contract_version="v1.0")

    def test_valid_semver_variants(self):
        assert DomainState(contract_version="0.1.0").contract_version == "0.1.0"
        assert DomainState(contract_version="10.20.30").contract_version == "10.20.30"

    def test_contract_version_none(self):
        d = DomainState(contract_version=None)
        assert d.contract_version is None


class TestProjectState:
    def test_empty(self):
        p = ProjectState()
        assert p.domains == {}

    def test_multiple_domains(self):
        p = ProjectState(
            domains={
                "holdings": DomainState(current_phase=4, iteration=2),
                "cashflows": DomainState(current_phase=1),
            }
        )
        assert len(p.domains) == 2
        assert p.domains["holdings"].current_phase == 4
        assert p.domains["cashflows"].current_phase == 1

    def test_json_round_trip(self):
        original = ProjectState(
            domains={
                "holdings": DomainState(
                    current_phase=6,
                    iteration=3,
                    contract_version="2.1.0",
                    resolutions={"CLR-001": ResolutionStatus.RESOLVED},
                )
            }
        )
        json_str = original.model_dump_json(indent=2)
        restored = ProjectState.model_validate_json(json_str)
        assert restored == original

    def test_json_structure_matches_spec(self):
        """Validate JSON output matches the structure defined in AGENTS.md."""
        state = ProjectState(
            domains={
                "holdings": DomainState(
                    current_phase=4,
                    iteration=2,
                    contract_version=None,
                    resolutions={"CLR-001": ResolutionStatus.RESOLVED, "CLR-002": ResolutionStatus.OPEN},
                )
            }
        )
        data = json.loads(state.model_dump_json())
        assert "domains" in data
        assert "holdings" in data["domains"]
        h = data["domains"]["holdings"]
        assert h["current_phase"] == 4
        assert h["iteration"] == 2
        assert h["contract_version"] is None
        assert h["resolutions"]["CLR-001"] == "resolved"
        assert h["resolutions"]["CLR-002"] == "open"


class TestLoadSave:
    def test_load_missing_file(self, tmp_path: Path):
        state = load_state(tmp_path / "nonexistent.json")
        assert state == ProjectState()

    def test_save_creates_parent_dirs(self, tmp_path: Path):
        path = tmp_path / "nested" / "dir" / "project.json"
        state = ProjectState(domains={"test": DomainState()})
        save_state(state, path)
        assert path.exists()

    def test_save_and_load_round_trip(self, tmp_path: Path):
        path = tmp_path / "project.json"
        original = ProjectState(
            domains={
                "holdings": DomainState(current_phase=3, iteration=1),
                "cashflows": DomainState(current_phase=7, contract_version="1.0.0"),
            }
        )
        save_state(original, path)
        loaded = load_state(path)
        assert loaded == original

    def test_load_corrupt_file(self, tmp_path: Path):
        path = tmp_path / "project.json"
        path.write_text("not valid json{{{")
        with pytest.raises(ValidationError):
            load_state(path)
