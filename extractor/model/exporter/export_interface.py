from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..setting import Setting

class ExportInterface(ABC):

    @classmethod
    @abstractmethod
    def export(cls, settings: List[Setting], output: Path) -> Path:
        pass