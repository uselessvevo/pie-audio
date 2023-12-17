import os.path
import re
import sys
import types
import importlib
import importlib.util


def import_by_path(path: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(os.path.basename(path).split(".")[0], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_import_string(string: str):
    return True if re.match(r'^([a-zA-Z|a-zA-Z\d+.]+)$', string) else False


def import_by_string(string: str, both: bool = False):
    """
    Import module by string:
    Args:
        string (str): <module path>.<ClassName>
        both (bool): if true - get import string and module, else - only module
    Returns:
        module (callable):
    """
    if not is_import_string(string):
        raise TypeError("Invalid import string")

    string = string.split('.')
    path, name = '.'.join(string[:-1]), string[-1]

    module = importlib.import_module(path)
    module = getattr(module, name)

    return (module, name) if both else module


def is_debug():
    trace = getattr(sys, 'gettrace', False)
    return True if trace() else False
