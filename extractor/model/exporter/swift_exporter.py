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
            out.write('import ProjectDescription\n\n')
            out.write('public typealias Path = String\n\n')
            out.write('public extension SettingsDictionary {\n')

            for s in settings:
                out.write('\n' + to_swift_code(s))

            out.write('\n\n}')
            out.write('\n\n')