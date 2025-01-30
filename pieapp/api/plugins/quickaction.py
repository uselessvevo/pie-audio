from PySide6.QtCore import QObject, Signal

from pieapp.api.exceptions import PieError
from pieapp.api.converter.models import MediaFile
from pieapp.widgets.buttons import Button, ButtonRole


class QuickAction(Button):
    sig_snapshots_loaded = Signal()
    sig_toggle_item_state = Signal(bool)
    sig_toggle_item_page_state = Signal(bool)

    def __int__(
        self,
        name: str,
        text: str,
        icon: "QIcon",
        callback: callable = None,
        before: str = None,
        after: str = None,
        enabled: bool = True,
        button_role: ButtonRole = ButtonRole.Default,
        parent: QObject = None,
        media_file_name: str = None
    ) -> None:
        super().__init__(parent)

        self._name = name
        self._button_state = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def button_state(self) -> bool:
        return self._button_state

    def get_title(self) -> str:
        raise NotImplementedError

    def get_icon(self) -> str:
        raise NotImplementedError

    def toggle_button(self, state: bool) -> None:
        self._button_state = state
        self.sig_toggle_item_page_state.emit(state)

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}, state: {self._button_state}>"
