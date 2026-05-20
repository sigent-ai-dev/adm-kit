"""ADM CLI — Analysis-Driven Modelling toolkit.

Bootstrap and manage ADM projects: discover, validate, and version
data schemas from messy real-world sources through seven sequential phases.
"""

__version__ = "0.0.1"

import typer

app = typer.Typer(
    name="adm",
    help="ADM Kit CLI — Analysis-Driven Modelling for legacy data sources.",
)


@app.command()
def init(
    domain: str = typer.Argument(..., help="Domain name (e.g., 'holdings', 'cashflows')"),
    source: str = typer.Option(None, "--source", help="Path to source data file(s)"),
    ai: str = typer.Option(
        "claude",
        "--ai",
        help="AI assistant: claude, gemini, copilot, cursor, q, windsurf",
    ),
    force: bool = typer.Option(False, "--force", help="Re-initialise existing domain"),
):
    """Initialise a new domain for ADM analysis."""
    from .init import run_init

    run_init(domain=domain, source=source, ai=ai, force=force)


@app.command()
def check():
    """Validate ADM state: phase gates, invariants, traceability."""
    from rich.console import Console

    console = Console()
    console.print("[bold]Checking ADM project state...[/]")
    console.print("[yellow]Not yet implemented — see issue #5[/]")


@app.command()
def status():
    """Show per-domain phase progression."""
    from rich.console import Console

    console = Console()
    console.print("[bold]ADM Domain Status[/]")
    console.print("[yellow]Not yet implemented — see issue #6[/]")


def main():
    app()
