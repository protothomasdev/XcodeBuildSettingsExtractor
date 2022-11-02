"""This module provides the extractor CLI."""

from pathlib import Path
from typing import Optional
import typer
from extractor import __app_name__, __version__
from .model.importer.importer import Importer
from .model.exporter.exporter import Exporter

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
    xc_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="The path to the local Xcode app.", 
    ),
    output_json: Optional[Path] = typer.Option(
        None,
        "--out-json",
        "-j",
        help="The path to the file the build settings should be exported to.", 
        file_okay=True,
        dir_okay=False)
) -> None:
    """Extracts the build settings from a given Xcode installation."""
    xcode = Path(xc_path)
    spec_file_paths = list(xcode.joinpath('Contents', 'PlugIns').rglob('*.xcspec'))
    settings = Importer.parse_paths(spec_file_paths)
    if output_json:
        Exporter.export_as_json(
            settings=settings,
            output=output_json
        )
        
def _showError(txt: str):
    typer.secho(txt, fg=typer.colors.RED)
    raise typer.Exit(1)
