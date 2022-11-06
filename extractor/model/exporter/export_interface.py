"""This module provides an interface to export settings."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..setting import Setting

class ExportInterface(ABC):
    """An interface to export settings."""

    @classmethod
    @abstractmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        """Exports the settings to a file."""
        pass