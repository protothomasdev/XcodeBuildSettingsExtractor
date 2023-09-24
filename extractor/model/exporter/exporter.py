"""This module provides an exporter."""

from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from .json_exporter import JSONExporter
from .swift_exporter import SwiftExporter
from ..setting import Setting

class Exporter:
    """A class that provides severarl methods to export settings."""

    @classmethod
    def export_as_json(cls, xcversion: str, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a JSON file."""
        JSONExporter.export(settings=settings, xcversion=xcversion, output=output)

    @classmethod
    def export_as_swift(cls, xcversion: str, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a Swift file."""
        SwiftExporter.export(settings=settings, xcversion=xcversion, output=output)