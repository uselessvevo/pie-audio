from __future__ import annotations

from PySide6.QtCore import QObject

from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.registries.toolbuttons.mixins import ToolButtonAccessorMixin
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry


class ContainerRegisterMixin:

    def register_object(self, target: QObject, *args, **kwargs) -> None:
        raise NotImplementedError

    def remove_object(self, target: QObject, *args, **kwargs) -> None:
        raise NotImplementedError


class ContainerRegisterAccessorMixin:
    """
    Container accessor
    """

    def register_on(self, parent_container: str, target: QObject, *args, **kwargs) -> None:
        """
        Register plugin on certain container by its name
        
        Args:
            parent_container (str): name of the parent container
            target (QObject): an object we want to register on `parent_container`
        """
        parent_container_instance = Registry(SysRegistry.Plugins).get(parent_container)
        if parent_container_instance and not isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Registry(SysRegistry.Plugins).get(parent_container)
        container_instance.register_object(target, *args, **kwargs)
    
    def remove_from(self, parent_container: str, target: QObject, *args, **kwargs) -> None:
        """
        Remove/unregister plugin from the container by its name
        
        Args:
            parent_container (str): name of the parent container
            target (QObject): an object we want to remove from the `parent_container`
        """
        parent_container_instance = Registry(SysRegistry.Plugins).get(parent_container)
        if parent_container_instance and isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Registry(SysRegistry.Plugins).get(parent_container)
        container_instance.remove_object(target, *args, **kwargs)


class CoreAccessorsMixin(
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    pass


class LayoutAccessorsMixins(
    MenuAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin
):
    pass
