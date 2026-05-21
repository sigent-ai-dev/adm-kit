"""Tests for auto-semver bumping."""

import json
from pathlib import Path

import pytest

from adm_cli.semver import bump_version, compute_next_version, determine_bump, parse_version


class TestParseVersion:
    def test_valid(self):
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_invalid(self):
        with pytest.raises(ValueError):
            parse_version("1.2")


class TestBumpVersion:
    def test_major(self):
        assert bump_version("1.2.3", "major") == "2.0.0"

    def test_minor(self):
        assert bump_version("1.2.3", "minor") == "1.3.0"

    def test_patch(self):
        assert bump_version("1.2.3", "patch") == "1.2.4"


class TestDetermineBump:
    def test_removed_field_is_major(self):
        old = {"properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name"]}
        new = {"properties": {"name": {"type": "string"}}, "required": ["name"]}
        assert determine_bump(old, new) == "major"

    def test_type_change_is_major(self):
        old = {"properties": {"age": {"type": "integer"}}, "required": ["age"]}
        new = {"properties": {"age": {"type": "string"}}, "required": ["age"]}
        assert determine_bump(old, new) == "major"

    def test_new_required_field_is_major(self):
        old = {"properties": {"name": {"type": "string"}}, "required": ["name"]}
        new = {"properties": {"name": {"type": "string"}, "email": {"type": "string"}}, "required": ["name", "email"]}
        assert determine_bump(old, new) == "major"

    def test_new_optional_field_is_minor(self):
        old = {"properties": {"name": {"type": "string"}}, "required": ["name"]}
        new = {"properties": {"name": {"type": "string"}, "nickname": {"type": "string"}}, "required": ["name"]}
        assert determine_bump(old, new) == "minor"

    def test_no_change_is_patch(self):
        schema = {"properties": {"name": {"type": "string"}}, "required": ["name"]}
        assert determine_bump(schema, schema) == "patch"

    def test_metadata_change_is_patch(self):
        old = {"properties": {"name": {"type": "string"}}, "required": ["name"], "title": "Old"}
        new = {"properties": {"name": {"type": "string"}}, "required": ["name"], "title": "New"}
        assert determine_bump(old, new) == "patch"


class TestComputeNextVersion:
    def test_first_version(self, tmp_path: Path):
        new_schema = tmp_path / "new.json"
        new_schema.write_text(json.dumps({"properties": {"name": {"type": "string"}}}))
        version, bump = compute_next_version(new_schema, None, None)
        assert version == "1.0.0"
        assert bump == "major"

    def test_minor_bump(self, tmp_path: Path):
        old_schema = tmp_path / "old.json"
        new_schema = tmp_path / "new.json"
        old_schema.write_text(json.dumps({"properties": {"name": {"type": "string"}}, "required": ["name"]}))
        new_schema.write_text(json.dumps({"properties": {"name": {"type": "string"}, "bio": {"type": "string"}}, "required": ["name"]}))
        version, bump = compute_next_version(new_schema, old_schema, "1.0.0")
        assert version == "1.1.0"
        assert bump == "minor"

    def test_major_bump(self, tmp_path: Path):
        old_schema = tmp_path / "old.json"
        new_schema = tmp_path / "new.json"
        old_schema.write_text(json.dumps({"properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name"]}))
        new_schema.write_text(json.dumps({"properties": {"name": {"type": "string"}}, "required": ["name"]}))
        version, bump = compute_next_version(new_schema, old_schema, "1.1.0")
        assert version == "2.0.0"
        assert bump == "major"
