from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QLabel

from pieapp.api.managers.registry import Managers
from pieapp.api.managers.structs import SysManager
from pieapp.api.plugins import PieObject
from pieapp.api.exceptions import PieException
from pieapp.api.managers.locales.helpers import translate
from pieapp.api.structs.layouts import Layout
from pieapp.api.structs.plugins import Plugin
from pieapp.helpers.qt import get_main_window


class LayoutManager(PieObject):
    name = Plugin.Layout

    @staticmethod
    def get_name() -> str:
        return translate("Layout")

    @staticmethod
    def get_description() -> str:
        return translate("Layout manager")

    def init(self) -> None:
        self._layout_manager = Managers(SysManager.Layout)

        main_layout = QGridLayout()
        main_layout.set_spacing(0)
        main_layout.set_contents_margins(0, 0, 0, 0)
        main_layout.set_alignment(Qt.AlignmentFlag.AlignHCenter)
        main_window = get_main_window()
        main_window.set_layout(main_layout)

        widget = QLabel()
        widget.set_layout(main_layout)
        main_window.set_central_widget(widget)

        self.add_layout(Layout.Main, main_layout)

    def add_layout(self, name: str, layout: QGridLayout) -> QGridLayout:
        if self._layout_manager.has_layout(name):
            raise PieException(f"Layout \"{layout}\" already exists")

        self._layout_manager.add_layout(name, layout)
        return layout

    def remove_layout(self, name: str) -> None:
        if not self._layout_manager.has_layout(name):
            raise PieException(f"Layout \"{name}\" not found")

        self._layout_manager.delete_layout(name)

    def get_layout(self, name: str) -> QGridLayout:
        if not self._layout_manager.has_layout(name):
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layout_manager.get_layout(name)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return LayoutManager(parent, plugin_path)
