from typing import Any
from types import ModuleType

import os
import importlib

from pieapp.utils.modules import import_by_path


class GlobalLoader:
    """
    Configuration modules loader
    """

    def __init__(self) -> None:
        # Dictionary of fields values (<field name>: <field value>)
        self.__dict__["_fields"]: dict[str, Any] = {}

    def import_module(self, import_path: str) -> None:
        """
        Load configuration module

        Args:
            import_path (str): configuration module import path
        """
        try:
            config_module: ModuleType = importlib.import_module(import_path)
        except ModuleNotFoundError as e:
            raise e

        self.load_module(config_module)

    def load_by_path(self, path: str) -> None:
        """
        A shortcut method to load module by path
        """
        if not os.path.exists(path):
            raise ModuleNotFoundError(f"Can't find module \"{path}\"")

        self.load_module(import_by_path(path))

    def load_module(self, config_module: ModuleType) -> None:
        """
        Process configuration module

        Args:
            config_module (ModuleType): configuration module
        """
        # Get all fields from the module
        module_attributes: dict[str, Any] = {
            k: v for (k, v) in config_module.__dict__.items() if k.isupper()
        }

        for field, value in module_attributes.items():
            self._fields[field] = value

    def __getattr__(self, field: str) -> Any:
        return self._fields.get(field)

    def __setattr__(self, field: str, value: Any) -> None:
        self._fields[field] = value


Global = GlobalLoader()
