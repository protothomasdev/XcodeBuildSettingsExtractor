import os
from pathlib import Path
import plistlib

class XcodeVersionExtractor:
    """A class to extract the xcode version from the version.plist file"""

    allowed_extensions = [".plist"]

    @classmethod
    def can_ingest(cls, path: Path) -> bool:
        """Tells if the given file can be parsed."""
        ext = path.suffix
        return ext in cls.allowed_extensions

    @classmethod
    def extract_version(cls, path: Path) -> str:
        if not cls.can_ingest(path):
            raise Exception("cannot ingest exception")
        with open(path, 'rb') as fp:
            pl = plistlib.load(fp)
            if not "CFBundleShortVersionString" in pl:
                raise Exception("cannot finf version string")
            return pl["CFBundleShortVersionString"]