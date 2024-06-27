from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QLabel

from pieapp.api.plugins import PiePlugin
from pieapp.helpers.qt import get_main_window
from pieapp.api.models.layouts import Layout
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.exceptions import PieException
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry
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
        self._layout_registry = Registry(SysRegistry.Layout)

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
        if self._layout_registry.contains(name):
            raise PieException(f"Layout \"{layout}\" already exists")

        self._layout_registry.add(name, layout)
        return layout

    def remove_layout(self, name: str) -> None:
        if not self._layout_registry.contains(name):
            raise PieException(f"Layout \"{name}\" not found")

        self._layout_registry.delete(name)

    def get_layout(self, name: str) -> QGridLayout:
        if not self._layout_registry.contains(name):
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layout_registry.get(name)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return LayoutManager(parent, plugin_path)
