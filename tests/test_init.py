"""Tests for `adm init` command."""

from pathlib import Path

import pytest

from adm_cli.constants import PHASE_DIRS
from adm_cli.init import run_init
from adm_cli.schema import load_state


class TestInitNewDomain:
    def test_creates_state_file(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        state_path = tmp_path / ".adm" / "project.json"
        assert state_path.exists()

    def test_state_has_correct_domain(self, tmp_path: Path):
        run_init(domain="holdings", source="./data/file.csv", ai="claude", force=False, project_dir=tmp_path)
        state = load_state(tmp_path / ".adm" / "project.json")
        assert "holdings" in state.domains
        assert state.domains["holdings"].current_phase == 1
        assert state.domains["holdings"].iteration == 1
        assert state.domains["holdings"].source_path == "./data/file.csv"
        assert state.domains["holdings"].contract_version is None

    def test_creates_all_artefact_directories(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        for phase_dir in PHASE_DIRS:
            assert (tmp_path / "artefacts" / "holdings" / phase_dir).is_dir()

    def test_installs_command_files(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        agent_dir = tmp_path / ".claude" / "commands"
        assert agent_dir.is_dir()
        assert (agent_dir / "adm.lineage.md").exists()
        assert (agent_dir / "adm.inventory.md").exists()
        assert (agent_dir / "adm.model.md").exists()
        # All 7 phase commands should be installed
        cmd_files = list(agent_dir.glob("adm.*.md"))
        assert len(cmd_files) >= 7


class TestInitExistingDomain:
    def test_refuses_without_force(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        with pytest.raises(SystemExit):
            run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)

    def test_allows_with_force(self, tmp_path: Path):
        run_init(domain="holdings", source="old.csv", ai="claude", force=False, project_dir=tmp_path)
        run_init(domain="holdings", source="new.csv", ai="claude", force=True, project_dir=tmp_path)
        state = load_state(tmp_path / ".adm" / "project.json")
        assert state.domains["holdings"].source_path == "new.csv"
        assert state.domains["holdings"].current_phase == 1


class TestMultiDomain:
    def test_additive(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        run_init(domain="cashflows", source=None, ai="claude", force=False, project_dir=tmp_path)
        state = load_state(tmp_path / ".adm" / "project.json")
        assert "holdings" in state.domains
        assert "cashflows" in state.domains

    def test_independent_artefact_trees(self, tmp_path: Path):
        run_init(domain="holdings", source=None, ai="claude", force=False, project_dir=tmp_path)
        run_init(domain="cashflows", source=None, ai="claude", force=False, project_dir=tmp_path)
        assert (tmp_path / "artefacts" / "holdings" / "1-lineage").is_dir()
        assert (tmp_path / "artefacts" / "cashflows" / "1-lineage").is_dir()


class TestAgentSupport:
    def test_claude_default(self, tmp_path: Path):
        run_init(domain="test", source=None, ai="claude", force=False, project_dir=tmp_path)
        assert (tmp_path / ".claude" / "commands" / "adm.lineage.md").exists()

    def test_gemini(self, tmp_path: Path):
        run_init(domain="test", source=None, ai="gemini", force=False, project_dir=tmp_path)
        assert (tmp_path / ".gemini" / "commands" / "adm.lineage.toml").exists()

    def test_copilot(self, tmp_path: Path):
        run_init(domain="test", source=None, ai="copilot", force=False, project_dir=tmp_path)
        assert (tmp_path / ".github" / "agents" / "adm-lineage.md").exists()

    def test_unknown_agent_fails(self, tmp_path: Path):
        with pytest.raises(SystemExit):
            run_init(domain="test", source=None, ai="unknown", force=False, project_dir=tmp_path)
