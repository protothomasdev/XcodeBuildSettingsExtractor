from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from .json_exporter import JSONExporter
from .swift_exporter import SwiftExporter
from ..setting import Setting

class Exporter:

    @classmethod
    def export_as_json(cls, settings: List[Setting], output: Path) -> Path:
        JSONExporter.export(settings=settings, output=output)

    @classmethod
    def export_as_swift(cls, settings: List[Setting], output: Path) -> Path:
        SwiftExporter.export(settings=settings, output=output)