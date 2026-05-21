"""Implementation of `adm status` — progression display."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.table import Table

from .constants import PHASE_NAMES
from .schema import ResolutionStatus, load_state


def run_status(project_dir: Path | None = None) -> None:
    """Display per-domain phase progression."""
    console = Console()
    root = project_dir or Path.cwd()
    state_path = root / ".adm" / "project.json"

    if not state_path.exists():
        console.print("[red]Error:[/] No ADM project found (.adm/project.json missing)")
        console.print("[dim]Run `adm init <domain>` to get started.[/]")
        raise SystemExit(1)

    state = load_state(state_path)

    if not state.domains:
        console.print("[yellow]No domains found.[/] Run `adm init <domain>` to get started.")
        return

    table = Table(title="ADM Domain Status")
    table.add_column("Domain", style="bold cyan")
    table.add_column("Phase")
    table.add_column("Iteration", justify="center")
    table.add_column("Contract", justify="center")
    table.add_column("Open Questions", justify="center")

    for name, domain in state.domains.items():
        phase_name = PHASE_NAMES.get(domain.current_phase, "Unknown")
        phase_display = f"{domain.current_phase} — {phase_name}"
        contract = domain.contract_version or "—"
        open_count = sum(
            1 for s in domain.resolutions.values() if s == ResolutionStatus.OPEN
        )
        open_display = str(open_count) if open_count > 0 else "[green]0[/green]"

        table.add_row(name, phase_display, str(domain.iteration), contract, open_display)

    console.print(table)
