"""ADM CLI — Analysis-Driven Modelling toolkit.

Bootstrap and manage ADM projects: discover, validate, and version
data schemas from messy real-world sources through seven sequential phases.
"""

__version__ = "0.1.0"

from typing import Optional

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
def check(
    domain: Optional[str] = typer.Option(None, "--domain", help="Check a specific domain only"),
):
    """Validate ADM state: phase gates, invariants, traceability."""
    from .check import run_check

    exit_code = run_check(domain_filter=domain)
    raise SystemExit(exit_code)


@app.command()
def status():
    """Show per-domain phase progression."""
    from .status import run_status

    run_status()


def main():
    app()
