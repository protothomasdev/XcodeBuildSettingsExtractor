"""This module provides the swift exporter."""

from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..swift_generator import to_swift_code
from ..setting import Setting

class SwiftExporter(ExportInterface):
    """An implementation of the ExportInterface to export settings to a swift file."""

    @classmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a Swift file."""
        with output.open('w') as out:
            for s in settings:
                out.write(to_swift_code(s))