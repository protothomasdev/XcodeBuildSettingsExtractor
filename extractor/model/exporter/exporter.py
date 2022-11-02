from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from .json_exporter import JSONExporter
from ..setting import Setting

class Exporter:

    @classmethod
    def export_as_json(cls, settings: List[Setting], output: Path) -> Path:
        JSONExporter.export(settings=settings, output=output)