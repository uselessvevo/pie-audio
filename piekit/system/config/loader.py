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
    Configuration modules loader
    """

    def __init__(self, import_paths: list[str], handlers: list[IHandler] = None):
        """
        Args:
            import_paths (list[str]): list of configuration modules import paths
            handlers (list[IHandler]): list of e-handlers
        """
        self._handlers = handlers
        self.load_module("piekit.system.config", False)
        for import_path in import_paths:
            self.load_module(import_path)

    def load_module(self, import_path: str, use_handlers: bool = True) -> None:
        """ 
        Load configuration module
        
        Args:
            import_path (str): configuration module import path
            use_handlers (boolean): use e-handlers or not
        """
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
                if use_handlers and self._handlers and name in annotated_attrs:
                    if annotated_attrs.get(name):
                        handler_class_name = annotated_attrs.get(name)
                        handler_class_name = f"{self._handlers.get(handler_class_name.__name__)}Handler"

                        if handler_class_name not in globals().keys():
                            raise HandlerNotImportedError(handler_class_name)

                        handler_instance = globals()[handler_class_name]()

                        if handler_instance not in self._handlers:
                            raise HandlerNotFoundError(handler_class_name)

                        handler_result = handler_instance(getattr(self, name), value)
                        setattr(self, name, handler_result)
                else:
                    setattr(self, name, value)


Config = ConfigLoader(
    import_paths=[os.environ.get("CONFIG_MODULE_NAME", "pieapp.config")], 
    handlers=[EDictHandler, EListHandler]
)
