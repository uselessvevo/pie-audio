from __future__ import annotations
from __feature__ import snake_case

from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QMessageBox

from pieapp.api.managers.configs.mixins import ConfigAccessorMixin
from pieapp.api.managers.locales.mixins import LocalesAccessorMixin
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.managers.menus.mixins import MenuAccessorMixin
from pieapp.api.managers.shortcuts.mixins import ShortcutAccessorMixin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.managers.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.managers.toolbuttons.mixins import ToolButtonAccessorMixin
from pieapp.api.plugins.types import Error
from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry


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
        parent_container_instance = Registries(SysRegistry.Plugins).get(parent_container)

        if parent_container_instance and not isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Registries(SysRegistry.Plugins).get(parent_container)
        container_instance.register_object(target, *args, **kwargs)
    
    def remove_from(self, parent_container: str, target: QObject, *args, **kwargs) -> None:
        """
        Remove/unregister plugin from the container by its name
        
        Args:
            parent_container (str): name of the parent container
            target (QObject): an object we want to remove from the `parent_container`
        """
        parent_container_instance = Registries(SysRegistry.Plugins).get(parent_container)

        if parent_container_instance and isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Registries(SysRegistry.Plugins).get(parent_container)
        container_instance.remove_object(target, *args, **kwargs)


class ErrorDialogMixin:
    """
    Shows an error in the message box.
    Requires `LocalesManager`

    How to use:

    1. Define a signal to the `error_handler` method
    2. Connect it like this

    ```py
    def connect_error_handler_method(self) -> None:
        self.sig_exception_occurred.connect(self.error_handler)
    ```
    """

    @Slot(Error)
    def error_handler(self, error: Error) -> None:
        message_box = QMessageBox()
        message_box.set_icon(QMessageBox.Icon.Critical)
        message_box.set_text(error.title)
        message_box.set_informative_text(error.description)
        message_box.set_window_title(translate("Error"))
        message_box.exec()


class CoreAccessorsMixin(
    ConfigAccessorMixin,
    LocalesAccessorMixin,
    ThemeAccessorMixin
):
    pass


class LayoutAccessorsMixins(
    ShortcutAccessorMixin,
    MenuAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin
):
    pass
