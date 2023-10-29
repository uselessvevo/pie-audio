from __future__ import annotations
from __feature__ import snake_case

from typing import Union

from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QApplication, QMessageBox

from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.plugins.types import Error
from piekit.managers.registry import Managers
from piekit.managers.structs import Section, SysManager
from piekit.widgets.messagebox import MessageCheckBox


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
        parent_container_instance = Managers(SysManager.Plugins).get(parent_container)

        if parent_container_instance and not isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(parent_container)
        container_instance.register_object(target, *args, **kwargs)
    
    def remove_from(self, parent_container: str, target: QObject, *args, **kwargs) -> None:
        """
        Remove/unregister plugin from the container by its name
        
        Args:
            parent_container (str): name of the parent container
            target (QObject): an object we want to remove from the `parent_container`
        """
        parent_container_instance = Managers(SysManager.Plugins).get(parent_container)

        if parent_container_instance and isinstance(parent_container_instance, ContainerRegisterMixin):
            raise KeyError(f"Container {parent_container} doesn't exist on {self.__class__.__name__}")

        container_instance = Managers(SysManager.Plugins).get(parent_container)
        container_instance.remove_object(target, *args, **kwargs)


class QuitDialogMixin(ConfigAccessorMixin, LocalesAccessorMixin):
    """
    Mixin that calls the MessageBox on exit. 
    Requires:
    * `ConfigAccessorMixin` with specified `exit_dialog_section` and `exit_dialog_key`
    * `LocalesAccessorMixin`
    """
    exit_dialog_section: Union[str, Section] = Section.User
    exit_dialog_key: str = "ui.show_exit_dialog"

    def close_event(self, event) -> None:
        if self.close_handler(True):
            event.accept()
        else:
            event.ignore()

    def close_handler(self, cancellable: bool = True) -> bool:
        show_exit_dialog = self.get_config(
            key="ui.show_exit_dialog",
            default=True,
            scope=Section.Root,
            section=self.exit_dialog_section
        )
        if cancellable and show_exit_dialog:
            message_box = MessageCheckBox(parent=self)
            message_box.set_check_box_text(self.get_translation("Don't show this message again?"))
            message_box.exec()
            if message_box.is_checked():
                self.set_config(self.exit_dialog_key, False, scope=Section.Root, section=Section.User)
                self.save_config(Section.Root, self.exit_dialog_section)

            if message_box.clicked_button() == message_box.no_button:
                return False

        QApplication.process_events()
        Managers.shutdown(full_house=True)

        return True


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
        message_box.set_window_title(self.get_translation("Error"))
        message_box.exec()
