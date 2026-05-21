"""Implementation of `adm check` — project state validation."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console

from .constants import PHASE_DIRS
from .schema import ProjectState, ResolutionStatus


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CheckFinding:
    severity: Severity
    domain: str
    message: str
    phase: int | None = None


@dataclass
class CheckReport:
    findings: list[CheckFinding] = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.ERROR)

    @property
    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.WARNING)

    @property
    def passed(self) -> bool:
        return self.errors == 0

    def add(self, severity: Severity, domain: str, message: str, phase: int | None = None) -> None:
        self.findings.append(CheckFinding(severity=severity, domain=domain, message=message, phase=phase))


def _check_artefact_dirs(report: CheckReport, domain: str, current_phase: int, root: Path) -> None:
    for i, phase_dir in enumerate(PHASE_DIRS, start=1):
        if i > current_phase:
            break
        path = root / "artefacts" / domain / phase_dir
        if path.is_dir():
            report.add(Severity.INFO, domain, f"artefacts/{domain}/{phase_dir}/ exists", phase=i)
        else:
            report.add(Severity.ERROR, domain, f"artefacts/{domain}/{phase_dir}/ missing (phase {i} claimed complete)", phase=i)


def _check_clarifications(report: CheckReport, domain: str, resolutions: dict[str, ResolutionStatus]) -> None:
    if not resolutions:
        report.add(Severity.INFO, domain, "No clarifications recorded")
        return
    open_count = sum(1 for s in resolutions.values() if s == ResolutionStatus.OPEN)
    resolved_count = sum(1 for s in resolutions.values() if s == ResolutionStatus.RESOLVED)
    if open_count > 0:
        open_ids = [k for k, v in resolutions.items() if v == ResolutionStatus.OPEN]
        report.add(Severity.WARNING, domain, f"{open_count} open clarifications ({', '.join(open_ids)})")
    else:
        report.add(Severity.INFO, domain, f"All {resolved_count} clarifications resolved — ready for ratchet")


def _check_invariants(report: CheckReport, domain: str, current_phase: int, root: Path) -> None:
    if current_phase < 3:
        return
    invariants_path = root / "artefacts" / domain / "3-invariants" / "invariants.py"
    if not invariants_path.exists():
        return
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(invariants_path), "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(root),
        )
        if result.returncode == 0:
            report.add(Severity.INFO, domain, f"Invariants: all passed")
        else:
            last_line = result.stdout.strip().split("\n")[-1] if result.stdout.strip() else "unknown result"
            report.add(Severity.WARNING, domain, f"Invariants: {last_line}")
    except subprocess.TimeoutExpired:
        report.add(Severity.WARNING, domain, "Invariants: timed out after 60s")
    except (OSError, subprocess.SubprocessError) as e:
        report.add(Severity.WARNING, domain, f"Invariants: execution error — {e}")


def run_check(domain_filter: str | None = None, project_dir: Path | None = None) -> int:
    """Execute the check command. Returns exit code (0=pass, 1=errors)."""
    console = Console()
    root = project_dir or Path.cwd()
    state_path = root / ".adm" / "project.json"

    if not state_path.exists():
        console.print("[red]Error:[/] No ADM project found (.adm/project.json missing)")
        console.print("[dim]Run `adm init <domain>` to create a project.[/]")
        raise SystemExit(1)

    try:
        state = ProjectState.model_validate_json(state_path.read_text())
    except ValidationError as e:
        console.print("[red]Error:[/] .adm/project.json is invalid:")
        console.print(f"[dim]{e}[/]")
        raise SystemExit(1)

    if not state.domains:
        console.print("[yellow]Warning:[/] No domains found in project state.")
        console.print("[dim]Run `adm init <domain>` to add a domain.[/]")
        raise SystemExit(0)

    report = CheckReport()

    domains_to_check = (
        {domain_filter: state.domains[domain_filter]}
        if domain_filter and domain_filter in state.domains
        else state.domains
    )

    if domain_filter and domain_filter not in state.domains:
        console.print(f"[red]Error:[/] Domain [bold]{domain_filter}[/] not found in project state.")
        raise SystemExit(1)

    console.print(f"[bold]ADM Check:[/] {root}")
    console.print()

    for domain_name, domain_state in domains_to_check.items():
        console.print(f"  [bold]{domain_name}[/] (phase {domain_state.current_phase}):")

        _check_artefact_dirs(report, domain_name, domain_state.current_phase, root)
        _check_clarifications(report, domain_name, domain_state.resolutions)
        _check_invariants(report, domain_name, domain_state.current_phase, root)

        # Print findings for this domain
        domain_findings = [f for f in report.findings if f.domain == domain_name]
        for finding in domain_findings:
            if finding.severity == Severity.ERROR:
                console.print(f"    [red]✗ {finding.message}[/]")
            elif finding.severity == Severity.WARNING:
                console.print(f"    [yellow]⚠ {finding.message}[/]")
            else:
                console.print(f"    [dim]✓ {finding.message}[/]")
        console.print()

    # Summary
    if report.passed:
        console.print(f"[bold green]Summary:[/] {report.errors} errors, {report.warnings} warnings — PASS")
    else:
        console.print(f"[bold red]Summary:[/] {report.errors} errors, {report.warnings} warnings — FAIL")

    return 0 if report.passed else 1
