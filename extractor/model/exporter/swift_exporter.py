from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..formatter import to_string
from ..setting import Setting

class SwiftExporter(ExportInterface):

    @classmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        with output.open('w') as out:
            for s in settings:
                out.write(to_string(s))