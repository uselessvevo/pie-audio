from PySide6.QtCore import QObject, Signal

from pieapp.api.exceptions import PieError
from pieapp.api.converter.models import MediaFile


class QuickAction(QObject):
    sig_snapshots_loaded = Signal()
    sig_toggle_item_state = Signal(bool)
    sig_toggle_config_page_state = Signal(bool)

    def __int__(self, name: str, snapshot_name: str, parent: QObject = None) -> None:
        super().__init__(parent)

        self._name = name
        self._is_blocked = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def init(self) -> None:
        pass

    def call(self) -> None:
        pass

    def get_title(self) -> str:
        raise NotImplementedError

    def get_icon(self) -> str:
        raise NotImplementedError

    def set_disabled(self, disabled: bool) -> None:
        self._is_blocked = disabled
        self.sig_toggle_config_page_state.emit(disabled)

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}>"
