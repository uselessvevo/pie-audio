from __feature__ import snake_case

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QStatusBar

from pieapp.api.exceptions import PieException
from pieapp.api.structs.plugins import Plugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin
from pieapp.api.structs.statusbar import StatusBarIndex


class StatusBar(PiePlugin, ThemeAccessorMixin):
    name = Plugin.StatusBar
    requires = [Plugin.Layout]

    def init(self) -> None:
        self._sb_widgets: dict[str, QWidget] = {}
        self._sb_perm_widgets: dict[str, QWidget] = {}
        self._status_bar: QStatusBar = self.parent().status_bar()
        self._status_bar.set_object_name("MainStatusBar")

    def show_message(self, message: str) -> None:
        self._status_bar.show_message(message)

    def insert_widget(self, name: str, widget: QObject, side: int = StatusBarIndex.Left) -> None:
        if name in self._sb_widgets:
            raise PieException(f"Status bar widget \"{name}\" is already registered")

        self._sb_widgets[name] = widget
        self._status_bar.insert_widget(side, widget)

    def insert_permanent_widget(self, name: str, widget: QObject, side: int = StatusBarIndex.Left) -> None:
        if name in self._sb_widgets:
            raise PieException(f"Status bar widget \"{name}\" is already registered")

        self._sb_perm_widgets[name] = widget
        self._status_bar.insert_permanent_widget(side, widget)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return StatusBar(parent, plugin_path)
