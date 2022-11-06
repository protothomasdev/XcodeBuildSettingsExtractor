"""This module provides an interface to import settings."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..setting import Setting

class ImportInterface(ABC):
    """An interface to import settings."""
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: Path) -> bool:
        """Tells if the given file can be parsed."""
        ext = path.suffix
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, paths: Path) -> List[Setting]:
        """Parses the contents of a file to a list of Settings."""
        pass

    @classmethod
    @abstractmethod
    def parse_paths(cls, paths: List[Path]) -> List[Setting]:
        """Parses the contents of a list of files to a list of Settings."""
        pass