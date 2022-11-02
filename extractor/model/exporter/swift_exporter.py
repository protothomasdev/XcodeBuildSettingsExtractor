from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..setting import Setting

class SwiftExporter(ExportInterface):

    @classmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        with output.open('w') as out:
            pass