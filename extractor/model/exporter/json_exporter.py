"""This module provides the json exporter."""

import json
from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..setting import Setting

class JSONExporter(ExportInterface):
    """An implementation of the ExportInterface to export settings to a json file."""

    @classmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a JSON file."""
        with output.open('w') as out:
            json.dump([s.__dict__ for s in settings], out, indent=4, sort_keys=True)