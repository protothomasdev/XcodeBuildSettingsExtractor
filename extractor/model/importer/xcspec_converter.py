"""This module provides methods to convert xcspec files to plists"""
from pathlib import Path
import subprocess
import tempfile, shutil, os

def convert(path: Path) -> str:
    """Convert a given .xcspec file to a .plist file."""
    if not path.suffix == ".xcspec":
        raise InvalidFileType
    
    temp_dir = tempfile.gettempdir()
    name = path.stem.replace(" ", "").lower()
    temp_xcspec = _create_temporary_copy(
        source=path,
        temp_dir=temp_dir,
        name=name + ".xcspec"
    )
    temp_plist = os.path.join(temp_dir, name + ".plist")

    subprocess.check_output(f"plutil -convert xml1 -o {temp_plist} {temp_xcspec}", shell=True)
    os.remove(temp_xcspec)
    return temp_plist


def _create_temporary_copy(source: Path, temp_dir, name: str) -> str:
    """Copy a file to a temp folder."""
    output = os.path.join(temp_dir, name)
    shutil.copy2(source, output)
    return output

class InvalidFileType(Exception):
    """Exception raised when the file type can not be handled"""