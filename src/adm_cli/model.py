"""Spec Kit handoff — seed a feature directory from a ratcheted contract."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


def generate_feature_json(
    domain: str,
    contract_version: str,
    contract_path: Path,
    schema_path: Path,
) -> dict:
    """Generate feature.json metadata for Spec Kit consumption."""
    return {
        "name": f"{domain}-engine",
        "source": "adm-kit",
        "domain": domain,
        "contract_version": contract_version,
        "contract_path": str(contract_path),
        "schema_path": str(schema_path),
        "generated": date.today().isoformat(),
    }


def generate_spec_seed(
    domain: str,
    contract_version: str,
    schema: dict,
    invariants: list[dict] | None = None,
) -> str:
    """Generate a Spec Kit-compatible spec.md seed from a contract schema."""
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    lines = [
        f"# Feature Specification: {domain.title()} Engine",
        "",
        f"**Source**: ADM Kit ratcheted contract v{contract_version}",
        f"**Generated**: {date.today().isoformat()}",
        "",
        "## Context",
        "",
        f"This specification was generated from the validated and ratcheted ADM contract for the `{domain}` data domain. "
        "All requirements trace back to discovered data invariants and validated schema fields.",
        "",
        "## Key Entities",
        "",
        f"### {domain.title()}Record",
        "",
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]

    for field_name, field_def in properties.items():
        field_type = field_def.get("type", "any")
        is_required = "Yes" if field_name in required else "No"
        description = field_def.get("description", "—")
        lines.append(f"| {field_name} | {field_type} | {is_required} | {description} |")

    lines.extend([
        "",
        "## Functional Requirements",
        "",
    ])

    for i, (field_name, field_def) in enumerate(properties.items(), start=1):
        constraint = ""
        if "minimum" in field_def:
            constraint = f" (minimum: {field_def['minimum']})"
        elif "pattern" in field_def:
            constraint = f" (pattern: `{field_def['pattern']}`)"
        lines.append(f"- **FR-{i:03d}**: System MUST store and validate `{field_name}`{constraint}")

    if invariants:
        lines.extend([
            "",
            "## Acceptance Criteria (from Invariants)",
            "",
        ])
        for inv in invariants:
            inv_id = inv.get("id", "INV-???")
            description = inv.get("description", inv.get("title", ""))
            lines.append(f"- **{inv_id}**: {description}")

    lines.extend([
        "",
        "## Traceability",
        "",
        "| Requirement | Source |",
        "|-------------|--------|",
    ])
    for i, field_name in enumerate(properties.keys(), start=1):
        lines.append(f"| FR-{i:03d} | contract.{field_name} |")

    lines.append("")
    return "\n".join(lines)


def seed_feature_directory(
    domain: str,
    contract_version: str,
    contract_path: Path,
    schema_path: Path,
    invariants_path: Path | None,
    specs_dir: Path,
) -> Path:
    """Create a Spec Kit feature directory seeded from the ADM contract.

    Returns the path to the created feature directory.
    """
    existing = sorted(specs_dir.glob("[0-9]*")) if specs_dir.exists() else []
    next_num = len(existing) + 1
    feature_dir = specs_dir / f"{next_num:03d}-{domain}-engine"
    feature_dir.mkdir(parents=True, exist_ok=True)

    schema = json.loads(schema_path.read_text())

    feature_meta = generate_feature_json(domain, contract_version, contract_path, schema_path)
    (feature_dir / "feature.json").write_text(json.dumps(feature_meta, indent=2) + "\n")

    invariants = None
    if invariants_path and invariants_path.exists():
        invariants = json.loads(invariants_path.read_text()).get("invariants", [])

    spec_content = generate_spec_seed(domain, contract_version, schema, invariants)
    (feature_dir / "spec.md").write_text(spec_content)

    return feature_dir
