import os
from pathlib import Path
import plistlib

from typing import List

from .xcspec_converter import convert

from .import_interface import ImportInterface
from ..setting import Setting
import typer

class PlistImporter(ImportInterface):
    allowed_extensions = [".plist",".xcspec"]

    @classmethod
    def parse(cls, path: Path) -> List[Setting]:
        settings = []
        if not cls.can_ingest(path):
            raise Exception("cannot ingest exception")
        with open(path, 'rb') as fp:
            pl = plistlib.load(fp)
            for d in pl:
                if not "Options" in d:
                    continue
                for option in d["Options"]:
                    
                    values = option.get("Values", [])
                    enum_values = cls.extract_values(values)

                    setting = Setting(
                        name=option.get("Name"),
                        key=option.get("Name"),
                        description=option.get("Description"),
                        type=option.get("Type"),
                        category=option.get("Category"),
                        default_value=option.get("DefaultValue"),
                        values=enum_values
                    )
                    settings.append(setting)

        return settings

    @classmethod
    def parse_paths(cls, paths: List[Path]) -> List[Setting]:
        settings = []
        for path in paths:
            if not cls.can_ingest(path):
                raise Exception("cannot ingest exception")
            if path.suffix == ".plist":
                settings += cls.parse(path)
            else:
                temp = convert(path)
                settings += cls.parse(Path(temp))
                os.remove(temp)
        return settings

    @classmethod
    def extract_values(cls, values: list) -> list:
        enum_values = []
        for value in values:
            if type(value) is str:
                enum_values.append(value)
            elif type(value) is dict:
                enum_values.append(value["Value"])
        return enum_values