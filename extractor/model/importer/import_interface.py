from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..setting import Setting


class ImportInterface(ABC):
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: Path) -> bool:
        ext = path.suffix
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, paths: Path) -> List[Setting]:
        pass

    @classmethod
    @abstractmethod
    def parse_paths(cls, paths: List[Path]) -> List[Setting]:
        pass