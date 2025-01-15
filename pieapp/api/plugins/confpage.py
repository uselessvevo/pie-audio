from typing import Union

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

from pieapp.api.exceptions import PieError
from pieapp.api.utils.qt import get_main_window


class ConfigPage(QObject):
    # Config page name
    name: str

    # Config page parent (to list in treeview)
    root: str

    # Set field as `True` to show page on top
    is_builtin_page: bool = False

    # Config page signals

    # Emit when all plugins are ready
    sig_plugins_ready = Signal()

    # Emit when application need to restart
    sig_restart_requested = Signal(str)

    # Emit when page is registered
    sig_page_registered = Signal(bool)

    # Emit to toggle apply button state
    sig_toggle_apply_button = Signal(bool)

    # Emit to block all form's elements and action buttons
    sig_toggle_config_page_state = Signal(bool)

    def __int__(self, name: str, parent: QObject = None) -> None:
        super().__init__(parent)

        self._is_modified = False
        self._is_blocked = False
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def init(self) -> None:
        """ Initialize page """

    def apply(self) -> None:
        """
        On apply event
        """
        pass

    def accept(self) -> None:
        """
        On accept event
        """
        raise PieError(f"Method `accept` in \"{self.name}\" configuration page must be implemented")

    def cancel(self) -> None:
        """
        On cancel event
        """
        raise PieError(f"Method `cancel` in \"{self.name}\" configuration page must be implemented")

    def set_page_state(self, disable: bool) -> None:
        pass

    def get_title(self) -> str:
        raise NotImplementedError

    def get_icon(self) -> Union[QIcon, None]:
        raise NotImplementedError

    def get_page_widget(self) -> QWidget:
        """
        Retrieve page widget
        """
        raise NotImplementedError

    @property
    def is_modified(self) -> bool:
        return self._is_modified

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def set_modified(self, modified: bool) -> None:
        self._is_modified = modified
        self.sig_toggle_apply_button.emit(modified)

    def set_disabled(self, disabled: bool, all_forms: bool = False) -> None:
        self._is_blocked = disabled
        self.sig_toggle_config_page_state.emit(disabled)

    def require_restart(self) -> None:
        self.sig_restart_requested.emit()
        main_window = get_main_window()
        if hasattr(main_window, "show_restart_dialog"):
            main_window.show_restart_dialog()

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}>"
