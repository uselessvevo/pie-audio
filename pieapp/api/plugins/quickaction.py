from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon

from pieapp.api.plugins import PiePlugin


class QuickAction(QObject):
    name: str

    def __init__(
        self,
        plugin: PiePlugin,
        enabled: bool = False,
        before: str = None,
        after: str = None,
    ) -> None:
        super(QuickAction, self).__init__(None)

        self._plugin_call_method = plugin.call
        self._plugin_name = plugin.name
        self._full_name = f"{plugin.name}_{self.name}"
        self._enabled = enabled
        self._media_file_name = None
        self._file_filter = None
        self._before = before
        self._after = after

    @property
    def plugin_call_method(self) -> callable:
        return self._plugin_call_method

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def before(self) -> str:
        return self._before

    @property
    def after(self) -> str:
        return self._after

    def get_tooltip(self) -> str:
        return ""

    def get_icon(self) -> QIcon:
        return QIcon()

    def on_click(self) -> None:
        raise NotImplementedError

    def get_enabled(self) -> tuple[bool, str]:
        """
        Reimplement this method.
        For example, you can filter file format to enable or disable button
        """
        return True, ""

    def set_disabled(self, state: bool) -> None:
        self.set_disabled(state)

    def set_snapshot_name(self, media_file_name: str):
        self._media_file_name = media_file_name

    def get_media_file_name(self) -> str:
        return self._media_file_name

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}, enabled: {self._enabled}>"
