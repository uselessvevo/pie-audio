import typing

from cloudykit.system import System
from cloudykit.managers.components.manager import ComponentsManager


class ComponentAccessor:
    """
    Component mixin
    """

    def __init__(self) -> None:
        self._components: ComponentsManager = System.registry.components

    def get_component(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._components.get(key, default)

    def register_component(self, key: typing.Any, data: typing.Any) -> None:
        self._components.set(key, data)

    def reload_component(self, key: typing.Any) -> None:
        self._components.delete(key)

    getComponent = get_component
    registerComponent = register_component
    reloadComponent = reload_component

    @property
    def components(self) -> ComponentsManager:
        return self._components
