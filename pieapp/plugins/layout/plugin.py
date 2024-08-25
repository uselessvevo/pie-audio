from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QLabel

from pieapp.api.plugins import PiePlugin
from pieapp.api.registries.layouts.manager import Layouts
from pieapp.utils.qt import get_main_window
from pieapp.api.models.layouts import Layout
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.exceptions import PieException
from pieapp.api.registries.locales.helpers import translate


class LayoutManager(PiePlugin):
    name = SysPlugin.Layout

    @staticmethod
    def get_name() -> str:
        return translate("Layout")

    @staticmethod
    def get_description() -> str:
        return translate("Layout manager")

    def init(self) -> None:
        main_layout = QGridLayout()
        main_layout.set_spacing(0)
        main_layout.set_contents_margins(0, 0, 0, 0)
        main_layout.set_alignment(Qt.AlignmentFlag.AlignHCenter)
        main_window = get_main_window()
        main_window.set_layout(main_layout)

        main_widget = QLabel()
        main_widget.set_layout(main_layout)
        main_window.set_central_widget(main_widget)

        Layouts.add(Layout.Main, main_layout)

    def add_layout(self, name: str, layout: QGridLayout, target_layout: QGridLayout,
                   row: int, col: int, alignment: Qt.AlignmentFlag) -> QGridLayout:
        if Layouts.contains(name):
            raise PieException(f"Layout \"{layout}\" already exists")

        layout.add_layout(target_layout, row, col, alignment=alignment)
        Layouts.add(name, layout)
        return layout

    def remove_layout(self, name: str) -> None:
        if not Layouts.contains(name):
            raise PieException(f"Layout \"{name}\" not found")

        layout = Layouts.get(name)
        Layouts.delete(name)

    def get_layout(self, name: str) -> QGridLayout:
        if not Layouts.contains(name):
            raise PieException(f"Can't find layout \"{name}\"")

        return Layouts.get(name)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return LayoutManager(parent, plugin_path)
