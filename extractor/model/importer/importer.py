from pathlib import Path
from typing import List

from .import_interface import ImportInterface
from .plist_importer import PlistImporter
from ..setting import Setting

class Importer(ImportInterface):
    importers = [PlistImporter]

    @classmethod
    def parse(cls, path: Path) -> List[Setting]:
        settings = []
        for importer in cls.importers:
            settings += importer.parse(path)
        return cls._clean(settings)

    @classmethod
    def parse_paths(cls, paths: List[Path]) -> List[Setting]:
        settings = []
        for importer in cls.importers:
            settings += importer.parse_paths(paths)
        return cls._clean(settings)

    @classmethod
    def _clean(cls, settings: List[Setting]) -> List[Setting]:
        cleaned_settings = list(set(settings))
        cleaned_settings = sorted(cleaned_settings, key=lambda x: x.key, reverse=False)
        return cleaned_settings
