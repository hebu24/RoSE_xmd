import importlib
import sys
from pathlib import Path
from types import ModuleType


def import_from_root(root: str | Path, module_name: str) -> ModuleType:
    path = str(Path(root).expanduser().resolve())
    if path not in sys.path:
        sys.path.insert(0, path)
    return importlib.import_module(module_name)
