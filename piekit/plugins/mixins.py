from typing import Union
from __feature__ import snake_case

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QApplication, QMessageBox

from piekit.plugins.types import Error
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.types import PluginTypes
from piekit.managers.registry import Managers
from piekit.managers.structs import Section, SysManager
from piekit.widgets.messagebox import MessageBox
from piekit.widgets.messagebox import MessageBox


class ContainerRegisterAccessor:
    """
    Main window accessor mixin
    """

    def register_on(self, container: str, target: PiePlugin) -> PiePlugin:
        """
        Register plugin on certain container by its name
        
        Args:
            container (str): name of the container
            target (PiePlugin): plugin instance

        Returns:
            A container instance
        """
        if not isinstance(target, PiePlugin):
            raise TypeError(f"Target {target.name} is not a `PiePlugin` based instance")
            
        if Managers(SysManager.Plugins).plugin_has_type(PluginTypes.Container):
            raise KeyError(f"Container {container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(container)
        container_instance.register_target(target)

        return container_instance
    
    def remove_from(self, container: str, target: str) -> PiePlugin:
        """
        Remove/unregister plugin from the container by its name
        
        Args:
            container (str): name of the container
            target (str): plugin name

        Returns:
            A container instance
        """
        if Managers(SysManager.Plugins).plugin_has_type(PluginTypes.Container):
            raise KeyError(f"Container {container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(container)
        container_instance.remove_target(target)

        return container_instance


class QuitMixin:
    """
    Mixin that calls the MessageBox on exit. 
    Requires `ConfigManager` and `ConfigAccessor`
    """
    show_exit_dialog_section: Union[str, Section] = Section.User

    def close_event(self, event) -> None:
        if self.close_handler(True):
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        if cancellable and self.get_config("ui.show_exit_dialog", True, self.show_exit_dialog_section):
            message_box = MessageBox(self)
            if message_box.clicked_button() == message_box.no_button:
                return False

        QApplication.process_events()
        Managers.shutdown(full_house=True)

        return True


class ErrorWindowMixin:
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
        message_box.set_window_title(self.get_translation("Error"))
        message_box.exec()
