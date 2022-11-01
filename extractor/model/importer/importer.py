from pathlib import Path
from typing import List

from .import_interface import ImportInterface
from .plist_importer import PlistImporter
from ..setting import Setting


class Importer(ImportInterface):
    importers = [PlistImporter]

    @classmethod
    def parse(cls, path: Path) -> List[Setting]:
        for importer in cls.importers:
            return importer.parse(path)

    @classmethod
    def parse_paths(cls, paths: List[Path]) -> List[Setting]:
        for importer in cls.importers:
            return importer.parse_paths(paths)
