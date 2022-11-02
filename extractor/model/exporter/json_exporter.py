import json
from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..setting import Setting

class JSONExporter(ExportInterface):

    @classmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        with output.open('w') as out:
            json.dump([s.__dict__ for s in settings], out, indent=4, sort_keys=True)