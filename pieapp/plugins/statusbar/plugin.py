from __feature__ import snake_case

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QStatusBar

from pieapp.api.exceptions import PieException
from pieapp.api.structs.plugins import Plugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.managers.themes.mixins import ThemeAccessorMixin


class StatusBarIndex:
    Left = 0
    Right = -1


class StatusBar(PiePlugin, ThemeAccessorMixin):
    name = Plugin.StatusBar
    requires = [Plugin.Layout]

    def show_message(self, message: str) -> None:
        self._status_bar.show_message(message)

    def add_widget(self, name: str, widget: QObject) -> None:
        self._status_widgets[name] = widget
        self._status_bar.add_widget(widget)

    def init(self) -> None:
        self._status_widgets: dict[str, QWidget] = {}
        self._status_bar: QStatusBar = self.parent().status_bar()
        self._status_bar.set_object_name("MainStatusBar")

    def add_status_widget(self, name: str, position: int, widget: QWidget) -> None:
        if name in self._status_widgets:
            raise PieException(f"Status bar widget \"{name}\" is already registered")

        self._status_widgets[name] = widget
        self._status_bar.insert_permanent_widget(position, widget)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return StatusBar(parent, plugin_path)
