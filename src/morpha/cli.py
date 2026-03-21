"""
Command-line interface for Morpha.

Commands
--------
info
    Display package information.
version
    Display version number.
"""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="morpha",
    help="Domain-agnostic data representation patterns for scientific computing.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def info() -> None:
    """Display package information."""
    from morpha import __version__

    table = Table(title="Morpha Package Info")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", __version__)
    table.add_row("Python", ">=3.12")

    modules = [
        ("components", "NumPy array subclasses with dimensions and metadata"),
        ("structures", "Abstract base classes for composite data structures"),
        ("coordinates", "Labeled axes with attribute validation"),
        ("creational", "Factory and Builder patterns"),
        ("io", "Saver/Loader for multiple file formats"),
    ]

    console.print(table)
    console.print("\n[bold]Modules:[/bold]")
    for name, desc in modules:
        console.print(f"  [cyan]{name}[/cyan]: {desc}")


@app.command()
def version() -> None:
    """Display version number."""
    from morpha import __version__

    console.print(f"morpha [green]{__version__}[/green]")


if __name__ == "__main__":
    app()
