"""Implementation of `adm init <domain>`."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .agents import adapt_command, command_filename
from .constants import AGENT_DIRS, PHASE_DIRS
from .schema import DomainState, load_state, save_state


def _templates_path() -> Path:
    """Get the path to bundled templates."""
    return Path(str(resources.files("adm_cli.templates")))


def run_init(
    domain: str,
    source: str | None,
    ai: str,
    force: bool,
    project_dir: Path | None = None,
) -> None:
    """Execute the init command."""
    console = Console()
    root = project_dir or Path.cwd()
    state_path = root / ".adm" / "project.json"

    state = load_state(state_path)

    if domain in state.domains and not force:
        console.print(
            f"[red]Error:[/] Domain [bold]{domain}[/] already exists. "
            f"Use [bold]--force[/] to re-initialise."
        )
        raise SystemExit(1)

    if ai not in AGENT_DIRS:
        console.print(
            f"[red]Error:[/] Unknown AI agent [bold]{ai}[/]. "
            f"Supported: {', '.join(AGENT_DIRS.keys())}"
        )
        raise SystemExit(1)

    domain_state = DomainState(source_path=source)
    state.domains[domain] = domain_state
    save_state(state, state_path)

    artefacts_dir = root / "artefacts" / domain
    created_dirs: list[str] = []
    for phase_dir in PHASE_DIRS:
        d = artefacts_dir / phase_dir
        d.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(d.relative_to(root)))

    templates = _templates_path()
    agent_dir = root / AGENT_DIRS[ai]
    agent_dir.mkdir(parents=True, exist_ok=True)
    commands_src = templates / "commands"
    installed_commands: list[str] = []
    for cmd_file in sorted(commands_src.glob("*.md")):
        base_name = cmd_file.stem
        adapted_content = adapt_command(cmd_file.read_text(), ai)
        dest_name = command_filename(base_name, ai)
        (agent_dir / dest_name).write_text(adapted_content)
        installed_commands.append(dest_name)

    # Summary output
    console.print()
    console.print(f"[bold green]ADM domain initialised:[/] {domain}")
    console.print()

    table = Table(title="Created", show_header=True)
    table.add_column("Item", style="cyan")
    table.add_column("Path")

    table.add_row("State file", str(state_path.relative_to(root)))
    for d in created_dirs:
        table.add_row("Artefact dir", d)
    for cmd in installed_commands:
        table.add_row("Command", f"{AGENT_DIRS[ai]}/{cmd}")

    console.print(table)
    console.print()

    if source:
        console.print(f"[dim]Source:[/] {source}")
    console.print(f"[dim]AI agent:[/] {ai}")
    console.print(f"[dim]Next step:[/] Run [bold]/adm.lineage[/] to begin Phase 1")
