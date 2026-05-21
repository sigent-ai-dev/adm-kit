"""Auto-semver bumping from JSON Schema diff."""

from __future__ import annotations

import json
from pathlib import Path


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse a semver string into (major, minor, patch)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid semver: {version!r}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def bump_version(current: str, bump_type: str) -> str:
    """Bump a semver version by type: major, minor, or patch."""
    major, minor, patch = parse_version(current)
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def determine_bump(old_schema: dict, new_schema: dict) -> str:
    """Compare two JSON Schemas and determine the semver bump type.

    - MAJOR: removed required fields, type changes on existing fields
    - MINOR: new optional fields added
    - PATCH: no schema change (metadata only)
    """
    old_props = old_schema.get("properties", {})
    new_props = new_schema.get("properties", {})
    old_required = set(old_schema.get("required", []))
    new_required = set(new_schema.get("required", []))

    removed_fields = set(old_props.keys()) - set(new_props.keys())
    added_fields = set(new_props.keys()) - set(old_props.keys())

    if removed_fields:
        return "major"

    removed_required = old_required - new_required
    if removed_required & set(old_props.keys()):
        pass  # relaxing required is minor, not major

    for field in set(old_props.keys()) & set(new_props.keys()):
        old_type = old_props[field].get("type")
        new_type = new_props[field].get("type")
        if old_type and new_type and old_type != new_type:
            return "major"

    added_required = new_required - old_required
    if added_required & added_fields:
        return "major"

    if added_fields:
        return "minor"

    if old_schema != new_schema:
        return "patch"

    return "patch"


def compute_next_version(
    new_schema_path: Path,
    prior_schema_path: Path | None,
    current_version: str | None,
) -> tuple[str, str]:
    """Compute the next contract version from schema comparison.

    Returns (next_version, bump_type).
    """
    if current_version is None or prior_schema_path is None or not prior_schema_path.exists():
        return "1.0.0", "major"

    new_schema = json.loads(new_schema_path.read_text())
    old_schema = json.loads(prior_schema_path.read_text())

    bump_type = determine_bump(old_schema, new_schema)
    next_ver = bump_version(current_version, bump_type)
    return next_ver, bump_type
