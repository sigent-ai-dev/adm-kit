"""Pydantic v2 state schema for .adm/project.json."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class ResolutionStatus(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"


class DomainState(BaseModel):
    """State for a single ADM domain."""

    current_phase: Annotated[int, Field(ge=1, le=7)] = 1
    iteration: Annotated[int, Field(ge=1)] = 1
    contract_version: str | None = None
    source_path: str | None = None
    resolutions: dict[str, ResolutionStatus] = Field(default_factory=dict)

    @field_validator("contract_version")
    @classmethod
    def validate_semver(cls, v: str | None) -> str | None:
        if v is None:
            return v
        import re

        if not re.match(r"^\d+\.\d+\.\d+$", v):
            raise ValueError(f"contract_version must be semver (MAJOR.MINOR.PATCH), got: {v!r}")
        return v


class ProjectState(BaseModel):
    """Root state model for .adm/project.json."""

    domains: dict[str, DomainState] = Field(default_factory=dict)


def load_state(path: Path) -> ProjectState:
    """Load project state from a JSON file."""
    if not path.exists():
        return ProjectState()
    return ProjectState.model_validate_json(path.read_text())


def save_state(state: ProjectState, path: Path) -> None:
    """Save project state to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(state.model_dump_json(indent=2) + "\n")
