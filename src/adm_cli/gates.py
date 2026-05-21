"""Phase gate enforcement for ADM domains."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

import yaml

from .init import PHASE_DIRS
from .schema import ProjectState, ResolutionStatus, save_state


def _load_phase_template_outputs(phase: int) -> list[str]:
    """Load required output filenames from a phase template's YAML frontmatter."""
    templates_path = Path(str(resources.files("adm_cli.templates"))) / "phases"
    phase_dir = PHASE_DIRS[phase - 1]
    template_file = templates_path / f"{phase_dir}.md"

    if not template_file.exists():
        return []

    content = template_file.read_text()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return []

    meta = yaml.safe_load(parts[1])
    if not meta or "expected_outputs" not in meta:
        return []

    return [
        o["filename"]
        for o in meta["expected_outputs"]
        if o.get("required", True)
    ]


def can_advance(
    domain: str,
    target_phase: int,
    state: ProjectState,
    project_dir: Path,
) -> tuple[bool, str]:
    """Check if a domain can advance to the target phase.

    Returns (allowed, reason) — reason explains why if blocked.
    """
    if domain not in state.domains:
        return False, f"Domain '{domain}' does not exist"

    domain_state = state.domains[domain]
    current = domain_state.current_phase

    if target_phase > 7:
        return False, "Cannot advance beyond phase 7"

    if target_phase != current + 1:
        return False, f"Can only advance to phase {current + 1}, not {target_phase} (no skipping)"

    # Check prior phase artefacts exist
    required_files = _load_phase_template_outputs(current)
    phase_dir_name = PHASE_DIRS[current - 1]
    artefact_dir = project_dir / "artefacts" / domain / phase_dir_name

    if not artefact_dir.is_dir():
        return False, f"Artefact directory missing: artefacts/{domain}/{phase_dir_name}/"

    missing = []
    for filename in required_files:
        if not (artefact_dir / filename).exists():
            # For versioned phases, check inside version subdirectories
            found_in_subdir = any(
                (artefact_dir / sub / filename).exists()
                for sub in artefact_dir.iterdir()
                if sub.is_dir()
            )
            if not found_in_subdir:
                missing.append(filename)

    if missing:
        return False, f"Missing required artefacts in {phase_dir_name}/: {', '.join(missing)}"

    # Ratchet gate: zero PENDING/OPEN resolutions
    if target_phase == 6:
        open_clrs = [
            k for k, v in domain_state.resolutions.items()
            if v == ResolutionStatus.OPEN
        ]
        if open_clrs:
            return False, f"Cannot ratchet: {len(open_clrs)} open clarifications ({', '.join(open_clrs)})"

    return True, "Gate passed"


def advance_phase(
    domain: str,
    state: ProjectState,
    state_path: Path,
) -> None:
    """Advance a domain's phase by 1 and save state atomically."""
    if domain not in state.domains:
        raise ValueError(f"Domain '{domain}' does not exist")

    domain_state = state.domains[domain]
    if domain_state.current_phase >= 7:
        raise ValueError(f"Domain '{domain}' is already at phase 7 (final)")

    domain_state.current_phase += 1
    save_state(state, state_path)
