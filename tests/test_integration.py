"""Integration test — full 7-phase ADM flow with sample data."""

import json
from pathlib import Path

import pytest

from adm_cli.check import run_check
from adm_cli.clarify import MergeMode, merge_clarifications, raise_clr, resolve_clr
from adm_cli.constants import PHASE_DIRS
from adm_cli.gates import advance_phase, can_advance
from adm_cli.init import run_init
from adm_cli.model import seed_feature_directory
from adm_cli.schema import load_state, save_state


DOMAIN = "holdings"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Initialise a project with a single domain."""
    run_init(domain=DOMAIN, source="./data/holdings.csv", ai="claude", force=False, project_dir=tmp_path)
    return tmp_path


def _artefact_dir(project: Path, phase: int) -> Path:
    return project / "artefacts" / DOMAIN / PHASE_DIRS[phase - 1]


def _write_phase_artefacts(project: Path, phase: int, files: dict[str, str]) -> None:
    """Simulate an AI agent producing artefacts for a phase."""
    phase_dir = _artefact_dir(project, phase)
    phase_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in files.items():
        (phase_dir / filename).write_text(content)


class TestFullSevenPhaseFlow:
    """Walk through all 7 phases, verifying state transitions and gates."""

    def test_complete_lifecycle(self, project: Path):
        state_path = project / ".adm" / "project.json"

        # === Phase 1: Lineage ===
        state = load_state(state_path)
        assert state.domains[DOMAIN].current_phase == 1

        # Simulate AI agent producing lineage artefacts
        _write_phase_artefacts(project, 1, {
            "lineage.md": "# Lineage\n\nHoldings data originates from portfolio system.",
            "lineage.json": json.dumps({
                "domain": DOMAIN,
                "origin": {"system": "portfolio-mgmt", "format": "csv", "frequency": "daily"},
                "touchpoints": [{"system": "portfolio-mgmt", "operation": "write"}],
                "consumers": [{"system": "reporting", "purpose": "NAV calculation"}],
                "open_questions": [{"id": "CLR-001", "question": "What is column X?", "status": "open"}],
            }),
        })

        # Raise a CLR and verify gate
        raise_clr(DOMAIN, state, state_path)
        allowed, _ = can_advance(DOMAIN, 2, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 2

        # === Phase 2: Inventory ===
        _write_phase_artefacts(project, 2, {
            "inventory.md": "# Inventory\n\n| ID | Column | Type |\n|---|---|---|\n| COL-001 | account_id | string |",
            "inventory.json": json.dumps({
                "domain": DOMAIN,
                "total_columns": 3,
                "files": [{"name": "holdings.csv", "columns": [
                    {"id": "COL-001", "name": "account_id", "observed_type": "string"},
                    {"id": "COL-002", "name": "balance", "observed_type": "float"},
                    {"id": "COL-003", "name": "currency", "observed_type": "string"},
                ]}],
            }),
        })

        allowed, _ = can_advance(DOMAIN, 3, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 3

        # === Phase 3: Invariants ===
        _write_phase_artefacts(project, 3, {
            "invariants.md": "# Invariants\n\nINV-001: account_id is unique",
            "invariants.py": (
                "import pytest\n\n"
                "def test_inv_001_account_id_unique():\n"
                "    assert True  # placeholder\n"
            ),
            "invariants.json": json.dumps({
                "domain": DOMAIN,
                "invariants": [
                    {"id": "INV-001", "title": "account_id unique", "category": "uniqueness", "status": "confirmed"},
                    {"id": "INV-002", "title": "balance >= 0", "category": "range", "status": "confirmed"},
                ],
            }),
        })

        allowed, _ = can_advance(DOMAIN, 4, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 4

        # === Phase 4: Thesis ===
        thesis_dir = _artefact_dir(project, 4) / "v1"
        thesis_dir.mkdir(parents=True)
        (thesis_dir / "thesis.md").write_text("# Thesis v1\n\nClaim: this model describes holdings.")
        (thesis_dir / "draft.py").write_text(
            "from pydantic import BaseModel, Field\n\n"
            "class HoldingsRecord(BaseModel):\n"
            "    account_id: str\n"
            "    balance: float = Field(ge=0)\n"
            "    currency: str\n"
        )
        schema = {
            "title": "HoldingsRecord",
            "properties": {
                "account_id": {"type": "string"},
                "balance": {"type": "number", "minimum": 0},
                "currency": {"type": "string"},
            },
            "required": ["account_id", "balance", "currency"],
        }
        (thesis_dir / "draft.schema.json").write_text(json.dumps(schema, indent=2))

        allowed, _ = can_advance(DOMAIN, 5, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 5

        # === Phase 5: Validate ===
        validation_dir = _artefact_dir(project, 5) / "v1"
        validation_dir.mkdir(parents=True)
        (validation_dir / "report.md").write_text("# Validation Report\n\nVerdict: PASS\n100% rows parsed.")
        (validation_dir / "report.json").write_text(json.dumps({
            "domain": DOMAIN,
            "thesis_version": 1,
            "total_records": 1000,
            "passed": 1000,
            "failed": 0,
            "verdict": "pass",
        }))

        # Resolve the CLR before ratcheting
        resolve_clr(DOMAIN, "CLR-001", state, state_path)

        allowed, _ = can_advance(DOMAIN, 6, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 6

        # === Phase 6: Ratchet ===
        contracts_dir = _artefact_dir(project, 6) / "v1.0.0"
        contracts_dir.mkdir(parents=True)
        (contracts_dir / "contract.py").write_text(
            '"""Contract: holdings v1.0.0"""\n'
            "from pydantic import BaseModel, Field\n\n"
            "CONTRACT_VERSION = '1.0.0'\n\n"
            "class HoldingsRecord(BaseModel):\n"
            "    account_id: str\n"
            "    balance: float = Field(ge=0)\n"
            "    currency: str\n"
        )
        (contracts_dir / "contract.schema.json").write_text(json.dumps(schema, indent=2))

        # Update state with contract version
        state.domains[DOMAIN].contract_version = "1.0.0"
        save_state(state, state_path)

        allowed, _ = can_advance(DOMAIN, 7, state, project)
        assert allowed is True
        advance_phase(DOMAIN, state, state_path)
        assert state.domains[DOMAIN].current_phase == 7

        # === Phase 7: Model (Spec Kit handoff) ===
        specs_dir = project / "specs"
        invariants_path = _artefact_dir(project, 3) / "invariants.json"
        schema_path = contracts_dir / "contract.schema.json"
        contract_path = contracts_dir / "contract.py"

        feature_dir = seed_feature_directory(
            domain=DOMAIN,
            contract_version="1.0.0",
            contract_path=contract_path,
            schema_path=schema_path,
            invariants_path=invariants_path,
            specs_dir=specs_dir,
        )

        assert feature_dir.exists()
        assert (feature_dir / "feature.json").exists()
        assert (feature_dir / "spec.md").exists()

        # Verify feature.json content
        feature_meta = json.loads((feature_dir / "feature.json").read_text())
        assert feature_meta["domain"] == DOMAIN
        assert feature_meta["contract_version"] == "1.0.0"

        # Verify spec.md has fields and invariants
        spec_content = (feature_dir / "spec.md").read_text()
        assert "account_id" in spec_content
        assert "balance" in spec_content
        assert "INV-001" in spec_content
        assert "INV-002" in spec_content
        assert "FR-001" in spec_content

        # === Final state check ===
        final_state = load_state(state_path)
        assert final_state.domains[DOMAIN].current_phase == 7
        assert final_state.domains[DOMAIN].contract_version == "1.0.0"
        assert final_state.domains[DOMAIN].iteration == 1


class TestGateEnforcementInFlow:
    """Verify gates block at the right points."""

    def test_cannot_skip_phases(self, project: Path):
        state_path = project / ".adm" / "project.json"
        state = load_state(state_path)
        allowed, reason = can_advance(DOMAIN, 3, state, project)
        assert allowed is False
        assert "no skipping" in reason.lower()

    def test_ratchet_blocked_by_open_clr(self, project: Path):
        state_path = project / ".adm" / "project.json"
        state = load_state(state_path)

        # Advance to phase 5 (write artefacts for phases 1-4, advance 4 times)
        for phase in range(1, 5):
            _write_phase_artefacts(project, phase, _minimal_artefacts(phase))
            advance_phase(DOMAIN, state, state_path)

        assert state.domains[DOMAIN].current_phase == 5

        # Write phase 5 artefacts so gate can check them
        _write_phase_artefacts(project, 5, _minimal_artefacts(5))

        # Raise an open CLR
        raise_clr(DOMAIN, state, state_path)

        # Try to advance to phase 6 (ratchet) — should be blocked by open CLR
        allowed, reason = can_advance(DOMAIN, 6, state, project)
        assert allowed is False
        assert "open clarifications" in reason.lower()


class TestClarifyPersistenceAcrossReRuns:
    """Verify resolutions survive phase re-runs."""

    def test_merge_preserves_resolved(self, project: Path):
        state_path = project / ".adm" / "project.json"
        state = load_state(state_path)

        # Raise and resolve a CLR
        clr_id = raise_clr(DOMAIN, state, state_path)
        resolve_clr(DOMAIN, clr_id, state, state_path)

        # Simulate phase re-run raising same + new CLRs
        merge_clarifications(DOMAIN, [clr_id, "CLR-002"], state, state_path, MergeMode.MERGE)

        # Original resolution preserved, new one is open
        from adm_cli.schema import ResolutionStatus
        assert state.domains[DOMAIN].resolutions[clr_id] == ResolutionStatus.RESOLVED
        assert state.domains[DOMAIN].resolutions["CLR-002"] == ResolutionStatus.OPEN


class TestCheckIntegration:
    """Verify adm check works against a real project."""

    def test_valid_project_passes(self, project: Path):
        exit_code = run_check(project_dir=project)
        assert exit_code == 0

    def test_missing_artefact_fails(self, project: Path):
        import shutil
        shutil.rmtree(project / "artefacts" / DOMAIN / "1-lineage")
        # adm check shouldn't fail on phase 1 dirs since the domain is AT phase 1
        # (it only checks dirs for phases <= current_phase)
        exit_code = run_check(project_dir=project)
        # Phase 1 dir missing but current_phase is 1 — this is an error
        assert exit_code == 1


def _minimal_artefacts(phase: int) -> dict[str, str]:
    """Return minimal artefact files for a phase (just enough to pass gate)."""
    files_by_phase = {
        1: {"lineage.md": "# Lineage", "lineage.json": "{}"},
        2: {"inventory.md": "# Inventory", "inventory.json": "{}"},
        3: {"invariants.md": "# Invariants", "invariants.py": "def test_pass(): pass", "invariants.json": "{}"},
        4: {"thesis.md": "# Thesis", "draft.py": "x=1", "draft.schema.json": "{}"},
        5: {"report.md": "# Report", "report.json": "{}"},
        6: {"contract.py": "x=1", "contract.schema.json": "{}"},
        7: {"feature.json": "{}", "spec.md": "# Spec"},
    }
    return files_by_phase.get(phase, {})
