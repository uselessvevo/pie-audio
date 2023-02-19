"""
Configuration manager that
loads data from piekit/system/config.py and %PIEAPP%/config.py
"""
import os
import types
import typing
import importlib

from piekit.system import types as ext_types

_HANDLERS_MAPPING: dict = {
    "EList": "handle_elist",
    "EDict": "handle_edict",
}


class ConfigLoader:
    """
    Loads configuration module
    and extends it by application's module
    """

    def __init__(self):
        self.load_module("piekit.system.config", False)
        if os.environ.get("CONFIG_MODULE_NAME", "pieapp.config"):
            self.load_module(os.environ.get("CONFIG_MODULE_NAME", "pieapp.config"), use_handlers=True)

    def load_module(
        self,
        import_path: str,
        use_handlers: bool = False
    ) -> None:
        try:
            config_module: types.ModuleType = importlib.import_module(import_path)
        except ModuleNotFoundError as e:
            raise e

        module_attributes: dict = config_module.__dict__
        annotated_attrs: dict = {
            k: v for (k, v) in config_module.__annotations__.items()
            if v.__name__ in dir(ext_types)
        }

        for name, attr in module_attributes.items():
            if name.isupper():
                if use_handlers and name in annotated_attrs:
                    if annotated_attrs.get(name):
                        handler_method = annotated_attrs.get(name)
                        handler_method = _HANDLERS_MAPPING.get(handler_method.__name__)
                        getattr(self, handler_method)(name, attr)
                else:
                    setattr(self, name, attr)

    def handle_elist(self, name, value: list[typing.Any]) -> None:
        """ Extendable list handler """
        old_value = getattr(self, name)
        old_value.extend(value)
        setattr(self, name, old_value)

    def handle_edict(self, name, value: dict) -> None:
        """ Extendable dict handler """
        old_value = getattr(self, name)
        old_value.update(**value)
        setattr(self, name, old_value)


Config = ConfigLoader()
