"""This module provides the extractor CLI."""

from pathlib import Path
from typing import Optional
import typer
from extractor import __app_name__, __version__
from extractor.model.importer.importer import Importer

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return

@app.command()
def extract(
    xc_path: str = typer.Argument(...)
) -> None:
    """Extracts the build settings from a given Xcode installation."""
    xcode = Path(xc_path)

    if not xcode.suffix == ".app":
        _showError(f'Path is not an application: {xcode.suffix}')
    if not xcode.exists():
         _showError('Xcode not found')
    else:
        spec_file_paths = list(xcode.joinpath('Contents', 'PlugIns').rglob('*.xcspec'))
        settings = Importer.parse_paths(spec_file_paths)
        
def _showError(txt: str):
    typer.secho(txt, fg=typer.colors.RED)
    raise typer.Exit(1)