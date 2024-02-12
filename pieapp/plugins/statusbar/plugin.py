from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from pieapp.api.plugins.decorators import on_plugin_event
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.structs.layouts import Layout
from pieapp.api.structs.plugins import Plugin
from pieapp.api.plugins.plugins import PiePlugin


class StatusBar(PiePlugin):
    name = Plugin.StatusBar
    requires = [Plugin.Layout]

    def show_message(self, message: str) -> None:
        self._status_bar_label.set_text(message)

    def init(self) -> None:
        self._main_grid = QGridLayout()
        self._status_bar = QWidget()
        self._status_bar_label = QLabel()
        self._status_bar_label.set_text("Sex")
        self._status_bar_label.set_style_sheet("QLabel {background-color: red}")
        self._status_bar.set_layout(self._main_grid)

    @on_plugin_event(target=Plugin.Layout)
    def on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(Plugin.Layout)
        main_layout = get_plugin(Plugin.Layout).get_layout(Layout.Main)
        if main_layout:
            main_layout.add_layout(self._main_grid, 0, 0, Qt.AlignmentFlag.AlignBottom)
            layout_manager.add_layout(self.name, self._main_grid)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return StatusBar(parent, plugin_path)
