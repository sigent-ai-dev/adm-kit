"""Tests for Spec Kit handoff (/adm.model)."""

import json
from pathlib import Path

from adm_cli.model import generate_feature_json, generate_spec_seed, seed_feature_directory


class TestGenerateFeatureJson:
    def test_structure(self):
        result = generate_feature_json(
            domain="holdings",
            contract_version="1.0.0",
            contract_path=Path("artefacts/holdings/6-contracts/v1.0.0/contract.py"),
            schema_path=Path("artefacts/holdings/6-contracts/v1.0.0/contract.schema.json"),
        )
        assert result["name"] == "holdings-engine"
        assert result["source"] == "adm-kit"
        assert result["domain"] == "holdings"
        assert result["contract_version"] == "1.0.0"
        assert "generated" in result


class TestGenerateSpecSeed:
    def test_includes_fields_as_requirements(self):
        schema = {
            "properties": {
                "account_id": {"type": "string", "pattern": "^ACC-\\d{4}$"},
                "balance": {"type": "number", "minimum": 0},
            },
            "required": ["account_id", "balance"],
        }
        result = generate_spec_seed("holdings", "1.0.0", schema)
        assert "FR-001" in result
        assert "account_id" in result
        assert "FR-002" in result
        assert "balance" in result
        assert "pattern" in result
        assert "minimum" in result

    def test_includes_invariants_as_ac(self):
        schema = {"properties": {"name": {"type": "string"}}, "required": ["name"]}
        invariants = [
            {"id": "INV-001", "description": "name is never null"},
            {"id": "INV-002", "description": "name is unique"},
        ]
        result = generate_spec_seed("holdings", "1.0.0", schema, invariants)
        assert "INV-001" in result
        assert "name is never null" in result
        assert "INV-002" in result

    def test_traceability_table(self):
        schema = {"properties": {"x": {"type": "string"}, "y": {"type": "integer"}}, "required": []}
        result = generate_spec_seed("test", "1.0.0", schema)
        assert "| FR-001 | contract.x |" in result
        assert "| FR-002 | contract.y |" in result


class TestSeedFeatureDirectory:
    def test_creates_directory_and_files(self, tmp_path: Path):
        schema_path = tmp_path / "contract.schema.json"
        schema_path.write_text(json.dumps({
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }))
        contract_path = tmp_path / "contract.py"
        contract_path.write_text("# contract\n")
        specs_dir = tmp_path / "specs"

        result = seed_feature_directory(
            domain="holdings",
            contract_version="1.0.0",
            contract_path=contract_path,
            schema_path=schema_path,
            invariants_path=None,
            specs_dir=specs_dir,
        )
        assert result.name == "001-holdings-engine"
        assert (result / "feature.json").exists()
        assert (result / "spec.md").exists()

    def test_sequential_numbering(self, tmp_path: Path):
        specs_dir = tmp_path / "specs"
        (specs_dir / "001-existing").mkdir(parents=True)

        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps({"properties": {}, "required": []}))
        contract_path = tmp_path / "contract.py"
        contract_path.write_text("")

        result = seed_feature_directory(
            domain="cashflows",
            contract_version="1.0.0",
            contract_path=contract_path,
            schema_path=schema_path,
            invariants_path=None,
            specs_dir=specs_dir,
        )
        assert result.name == "002-cashflows-engine"

    def test_includes_invariants(self, tmp_path: Path):
        schema_path = tmp_path / "schema.json"
        schema_path.write_text(json.dumps({"properties": {"x": {"type": "string"}}, "required": []}))
        contract_path = tmp_path / "contract.py"
        contract_path.write_text("")
        inv_path = tmp_path / "invariants.json"
        inv_path.write_text(json.dumps({"invariants": [{"id": "INV-001", "description": "x is unique"}]}))
        specs_dir = tmp_path / "specs"

        result = seed_feature_directory(
            domain="test",
            contract_version="2.0.0",
            contract_path=contract_path,
            schema_path=schema_path,
            invariants_path=inv_path,
            specs_dir=specs_dir,
        )
        spec_content = (result / "spec.md").read_text()
        assert "INV-001" in spec_content
        assert "x is unique" in spec_content
