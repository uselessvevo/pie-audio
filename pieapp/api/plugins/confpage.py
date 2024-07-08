from typing import Union

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

from pieapp.api.exceptions import PieException
from pieapp.helpers.qt import get_main_window


class ConfigPage(QObject):
    name: str
    root: str

    # Show page on top
    is_builtin_page: bool = False

    # Emit when all plugins are ready
    sig_plugins_ready = Signal()
    
    # Emit when application need to restart
    sig_restart_requested = Signal(str)
    
    # Emit when page is registered
    sig_page_registered = Signal(bool)
    
    # Emit to toggle apply button state
    sig_toggle_apply_button = Signal(bool)

    def __int__(self, parent=None) -> None:
        super().__init__(parent)

        self._is_modified = False

    def init(self) -> None:
        """ Initialize page """

    def accept(self) -> None:
        """ On accept event """
        raise PieException(f"Method `accept` in \"{self.name}\" configuration page must be implemented")

    def cancel(self) -> None:
        """ On cancel event """
        raise PieException(f"Method `cancel` in \"{self.name}\" configuration page must be implemented")

    def get_title(self) -> str:
        raise NotImplementedError

    def get_icon(self) -> Union[QIcon, None]:
        return None

    def get_page_widget(self) -> QWidget:
        """ Render page """
        raise PieException(f"Method f`{self.__qualname__}` in \"{self.name}\" configuration page must be implemented")

    @property
    def is_modified(self) -> bool:
        return self._is_modified

    def set_modified(self, state: bool) -> None:
        self._is_modified = state
        self.sig_toggle_apply_button.emit(state)

    def require_restart(self) -> None:
        main_window = get_main_window()
        if hasattr(main_window, "show_restart_dialog"):
            main_window.show_restart_dialog()

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}, parent: {self.root}>"
