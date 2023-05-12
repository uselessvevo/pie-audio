"""
Layout object
"""
from piekit.plugins.plugins import PiePlugin


class ContainerRegisterMixins:

    def __init__(self) -> None:
        self._objects: dict[str, PiePlugin] = {}
    
    def register_target(self, target: PiePlugin) -> None:
        """
        Register `PiePlugin` instance and register it in `_objects` dictionary
        """
        raise NotImplementedError("Method `register_target` must be implemented")

    def remove_target(self, target: PiePlugin) -> None:
        """
        Remove `PiePlugin` instance and remove it from `_objects` dictionary
        """
        raise NotImplementedError("Method `remove_target` must be implemented")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> (id: {id(self)}, parent: {self._parent})"
