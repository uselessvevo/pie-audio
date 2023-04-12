import warnings
import importlib
from typing import Any
from types import ModuleType

from piekit.config.types import Lock


class ConfigLoader:
    """
    Configuration modules loader
    """

    def __init__(self) -> None:
        self.__dict__["locked_attributes"]: dict[str, bool] = {}

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

    def load_module(self, config_module: ModuleType) -> None:
        """
        Process configuration module

        Args:
            config_module (ModuleType): configuration module
        """
        temp_locked_attributes: list[str] = []
        module_attributes: dict[str, Any] = {
            k: v for (k, v) in config_module.__dict__.items() if k.isupper()
        }
        module_locked_attributes: dict = {
            k: v for (k, v) in getattr(config_module, "__annotations__", {}).items()
            if k.isupper() and issubclass(v, Lock)
        }

        for name, value in module_attributes.items():
            if name in module_locked_attributes:
                if name in self.locked_attributes:
                    warnings.warn(f"{name} is locked - you can't change its value")
                    continue
                else:
                    temp_locked_attributes.append(name)

            setattr(self, name, value)

        for attr in temp_locked_attributes:
            self.locked_attributes[attr] = True

    def __setattr__(self, key, value):
        if key in self.locked_attributes:
            warnings.warn(f"Can't change the value of the locked attribute {key}")
        else:
            self.__dict__[key] = value


Config = ConfigLoader()