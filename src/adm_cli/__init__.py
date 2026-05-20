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
):
    """Initialise a new domain for ADM analysis."""
    from rich.console import Console
    console = Console()
    console.print(f"[bold green]Initialising ADM domain:[/] {domain}")
    if source:
        console.print(f"[dim]Source:[/] {source}")
    console.print(f"[dim]AI assistant:[/] {ai}")
    # TODO: Implement domain scaffolding
    console.print("[yellow]Not yet implemented — see CONTRIBUTING.md[/]")


@app.command()
def check():
    """Validate ADM state: phase gates, invariants, traceability."""
    from rich.console import Console
    console = Console()
    console.print("[bold]Checking ADM project state...[/]")
    # TODO: Implement validation
    console.print("[yellow]Not yet implemented — see CONTRIBUTING.md[/]")


@app.command()
def status():
    """Show per-domain phase progression."""
    from rich.console import Console
    console = Console()
    console.print("[bold]ADM Domain Status[/]")
    # TODO: Implement status display
    console.print("[yellow]Not yet implemented — see CONTRIBUTING.md[/]")


def main():
    app()
