# core/utils/module_loader.py

import importlib
import pkgutil
import sys
from pathlib import Path

def import_modules(package_name: str):
    """
    Auto-import all *_api.py modules under the specified package
    to trigger decorators (like Api route registration).

    :param package_name: Package/folder to search for modules
                         e.g., 'webapi'
    """
    # Ensure the parent directory of the package is in sys.path
    package_path = Path(__file__).parent.parent.parent / package_name
    if str(package_path.parent) not in sys.path:
        sys.path.append(str(package_path.parent))

    for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
        if name.endswith("_api"):
            full_module_name = f"{package_name}.{name}"
            importlib.import_module(full_module_name)
            print(f"Imported {full_module_name}")
