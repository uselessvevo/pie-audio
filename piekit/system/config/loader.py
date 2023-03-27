"""
Configuration manager that
loads data from piekit/system/config.py and %PIEAPP%/config.py
"""
import os
import types
import importlib

from piekit.system import types as ext_types
from piekit.system.config.handlers import IHandler, EDictHandler, EListHandler
from piekit.system.config.exceptions import HandlerNotFoundError, HandlerNotImportedError


class ConfigLoader:
    """
    Loads configuration module
    and extends it by application's module
    """

    handlers: tuple[IHandler] = None

    def __init__(self, handlers: tuple[IHandler] = None):
        self.handlers = handlers
        self._load_module("piekit.system.config", False)
        if os.environ.get("CONFIG_MODULE_NAME", "pieapp.config"):
            self._load_module(os.environ.get("CONFIG_MODULE_NAME", "pieapp.config"))

    def _load_module(self, import_path: str) -> None:
        try:
            config_module: types.ModuleType = importlib.import_module(import_path)
        except ModuleNotFoundError as e:
            raise e

        module_attributes: dict = config_module.__dict__
        annotated_attrs: dict = {
            k: v for (k, v) in config_module.__annotations__.items()
            if v.__name__ in dir(ext_types)
        }

        for name, value in module_attributes.items():
            if name.isupper():
                if self.handlers and name in annotated_attrs:
                    if annotated_attrs.get(name):
                        handler_class_name = annotated_attrs.get(name)
                        handler_class_name = f"{self.handlers.get(handler_class_name.__name__)}Handler"

                        if not handler_class_name not in globals().keys():
                            raise HandlerNotImportedError(handler_class_name)

                        handler_instance = globals()[handler_class_name]()

                        if not handler_instance in self.handlers:
                            raise HandlerNotFoundError(handler_class_name)

                        handler_result = handler_instance(getattr(self, name), value)
                        setattr(self, name, handler_result)
                else:
                    setattr(self, name, value)


Config = ConfigLoader(handlers=(EDictHandler, EListHandler))
