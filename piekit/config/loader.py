import warnings
import importlib
from typing import Any
from types import ModuleType

from piekit.config.types import Annotated


class ConfigLoader:
    """
    Configuration modules loader
    """

    def __init__(self) -> None:
        # Dictionary of handlers (<handler name>: <handler instance>)
        self.__dict__["_handlers"]: dict[str, Any] = {}

        # Dictionary of fields to handlers relation (<field name>: <handler name>)
        self.__dict__["_fields_handlers"]: dict[str, str] = {}

    def add_handlers(self, *handlers: Annotated) -> None:
        for handler in handlers:
            if handler in self._handler:
                raise AttributeError(f"Handler {handler} is already added")

            self._handlers[handler.__class__.__name__] = handler()

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
        # Get all fields from the module
        module_attributes: dict[str, Any] = {
            k: v for (k, v) in config_module.__dict__.items() if k.isupper()
        }
        
        # Get all fields with `Annotated` type annotation
        module_annotated_attributes: dict = {
            k: v for (k, v) in getattr(config_module, "__annotations__", {}).items()
            if k.isupper() 
            and issubclass(v, Annotated) 
            and v.__class__.__name__ in self._handlers
        }

        for field, value in module_attributes.items():
            if field in module_annotated_attributes:
                self._fields_handlers[field] = module_annotated_attributes.get(field)

            setattr(self, field, value)

    def __setattr__(self, field: str, value: Any) -> None:
        if field in self._fields_handlers:
            handler_name = self._fields_handlers.get(field)
            handler_instance: Annotated = self._handlers.get(handler_name)
            try:
                handler_instance.set(field, value)
            except Exception as e:
                warnings.warn(e)
        else:
            self.__dict__[field] = value


Config = ConfigLoader()
