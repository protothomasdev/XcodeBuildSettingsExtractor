"""This module provides the json exporter."""

import json
from pathlib import Path
from typing import List
from .export_interface import ExportInterface
from ..setting import Setting

class JSONExporter(ExportInterface):
    """An implementation of the ExportInterface to export settings to a json file."""

    @classmethod
    def export(cls, xcversion: str, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a JSON file."""
        with output.open('w') as out:
            settings_dict = [s.__dict__ for s in settings]
            dict_to_dump = {
                "xcode_version": xcversion,
                "settings": settings_dict
            }
            json.dump(dict_to_dump, out, indent=4, sort_keys=True)