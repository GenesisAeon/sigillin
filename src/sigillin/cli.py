"""Sigillin CLI – sig validate / render / inspect / bridge."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .core import Sigil

app = typer.Typer(
    name="sig",
    help="Sigillin CLI – poetic-symbolic sigil engine",
    add_completion=False,
)
console = Console()

_CREP_KEYS = ("coherence", "resonance", "emergence", "poetics")


@app.command()
def validate(
    path: Path = typer.Argument(..., help="Path to sigil file (YAML/JSON/Markdown)"),
) -> None:
    """Validate a sigil against the CREP schema (Coherence · Resonance · Emergence).
    """
    if not path.exists():
        console.print(f"[bold red]✗ File not found:[/] {path}")
        raise typer.Exit(1)
    sigil = Sigil(path)
    if sigil.validate_crep():
        console.print(f"[bold green]✓ Sigil valid – CREP-aligned[/]  ({path.name})")
    else:
        missing = [k for k in _CREP_KEYS if k not in sigil.data]
        console.print(f"[bold red]✗ Sigil invalid[/]  ({path.name})")
        console.print(f"  Missing CREP keys: [yellow]{', '.join(missing)}[/]")
        raise typer.Exit(1)


@app.command()
def render(
    path: Path = typer.Argument(..., help="Path to sigil file"),
    depth: float = typer.Option(0.618, help="Fractal resonance depth (default: φ)"),
) -> None:
    """Render the MandalaMap resonance spectrum for a sigil."""
    if not path.exists():
        console.print(f"[bold red]✗ File not found:[/] {path}")
        raise typer.Exit(1)
    sigil = Sigil(path)
    spectrum = sigil.render_mandala(depth)
    console.print(f"[bold magenta]Mandala resonance peak:[/]  {spectrum.max():.4f}")
    console.print(f"[bold magenta]Mandala resonance mean:[/]  {spectrum.mean():.4f}")
    console.print(sigil.bind_to_field())


@app.command()
def inspect(
    path: Path = typer.Argument(..., help="Path to sigil file"),
) -> None:
    """Inspect sigil fields in a rich table."""
    if not path.exists():
        console.print(f"[bold red]✗ File not found:[/] {path}")
        raise typer.Exit(1)
    sigil = Sigil(path)
    table = Table(
        title=f"Sigil: {path.name}",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Key", style="cyan")
    table.add_column("Value")
    for k, v in sigil.data.items():
        table.add_row(str(k), str(v))
    console.print(table)
    crep_status = "[green]✓ valid[/]" if sigil.validate_crep() else "[red]✗ invalid[/]"
    console.print(f"CREP status: {crep_status}")


@app.command()
def bridge(
    provider: str = typer.Argument("openai", help="Provider name for bridge"),
) -> None:
    """Create a self-referential provider bridge."""
    console.print(
        f"[bold cyan]Selfmeta bridge for [white]{provider}[/white] created[/]"
    )


if __name__ == "__main__":
    app()
