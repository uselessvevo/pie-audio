import typing

from cloudykit.system.manager import System
from cloudykit.managers.components.manager import ComponentsManager


class ComponentAccessor:
    """
    Component mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._components: ComponentsManager = System.registry.components

    def get_component(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._components.get(self._section, key, default)

    def set_component(self, key: typing.Any, data: typing.Any) -> None:
        self._components.set(self._section, key, data)

    def delete_component(self, key: typing.Any) -> None:
        self._components.delete(self._section, key)

    getComponent = get_component
    setComponent = set_component
    deleteComponent = delete_component

    @property
    def components(self) -> ComponentsManager:
        return self._components
