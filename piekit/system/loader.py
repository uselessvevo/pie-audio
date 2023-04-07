import types
import warnings
import importlib

from piekit.system import PieException
from piekit.system.types import etype


class ConfigLoader:
    """
    Configuration modules loader
    """

    def __init__(self) -> None:
        self._etypes: list[etype] = []

    def add_type(self, etype: etype) -> None:
        if not issubclass(etype, etype):
            raise TypeError(f"Type {etype.__class__.__name__} is not a e-type based class")

        if etype in self._etypes:
            raise TypeError(f"Type {etype.__class__.__name__} already added")

        self._etypes.append(etype)

    def load_module(self, import_path: str, use_etypes: bool = True) -> None:
        """ 
        Load configuration module
        
        Args:
            import_path (str): configuration module import path
            use_etypes (boolean): use e-types or not
        """
        try:
            config_module: types.ModuleType = importlib.import_module(import_path)
        except ModuleNotFoundError as e:
            raise e

        module_attributes: dict = {
            k: v for (k, v) in config_module.__dict__.items()
            if k.isupper()
        }
        etyped_attributes: dict = {
            k: v for (k, v) in config_module.__annotations__.items()
            if k.isupper() and v in self._etypes
        }

        for name, value in module_attributes.items():
            if use_etypes and etyped_attributes.get(name):
                etype_instance = etyped_attributes.get(name)()
                if etype_instance.frozen is True:
                    warnings.warn(
                        f"etype {name} is frozen, "
                        "that means you cant't overwrite value of it"
                    )
                    continue
                try:
                    handler_result = etype_instance(getattr(self, name), value)
                    setattr(self, name, handler_result)
                except Exception as e:
                    raise PieException(str(e))
            else:
                # Handle built-in or other types
                setattr(self, name, value)


Config = ConfigLoader()
