from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QHBoxLayout

from pieapp.api.plugins import PiePlugin
from pieapp.api.utils.qt import get_main_window
from pieapp.api.models.layouts import Layout
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.exceptions import PieError
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.layouts.registry import LayoutRegistry


class MainLayoutPlugin(PiePlugin):
    name = SysPlugin.Layout

    @staticmethod
    def get_name() -> str:
        return translate("Layout")

    @staticmethod
    def get_description() -> str:
        return translate("Layout manager")

    def init(self) -> None:
        self._root_layout = QGridLayout()
        self._root_layout.set_spacing(0)
        self._root_layout.set_contents_margins(0, 0, 0, 0)

        main_window = get_main_window()
        main_window.set_layout(self._root_layout)
        self.set_central_widget(QLabel())

        tools_layout = QHBoxLayout()
        main_layout = QGridLayout()
        info_layout = QHBoxLayout()

        self._root_layout.add_layout(tools_layout, 0, 0)
        self._root_layout.add_layout(main_layout, 1, 0)
        self._root_layout.add_layout(info_layout, 2, 0)

        self.add_layout(Layout.Tools, tools_layout, Layout.Tools)
        self.add_layout(Layout.Main, main_layout, Layout.Main)
        self.add_layout(Layout.Info, info_layout, Layout.Info)

    def set_central_widget(self, widget: "QWidget") -> None:
        main_window = get_main_window()
        widget.set_layout(self._root_layout)
        main_window.set_central_widget(widget)

    def add_layout(
        self,
        child_layout_name: str,
        child_layout: "QLayout",
        parent_layout_name: str
    ) -> None:
        """
        Args:
            child_layout_name (str): Name of the layout
            child_layout (QGridLayout): Child layout object
            parent_layout_name (str): Parent layout name
        """
        if LayoutRegistry.contains(child_layout_name):
            raise PieError(f"Layout \"{parent_layout_name}\" already exists")

        LayoutRegistry.add(child_layout_name, child_layout, parent_layout_name)

    def remove_layout(self, name: str, unregister_children: bool = True) -> None:
        if not LayoutRegistry.contains(name):
            raise PieError(f"Layout \"{name}\" not found")

        # TODO: Remove all children layout from the parent layout
        # children = LayoutRegistry.get_children(name)
        LayoutRegistry.delete(name)

    def get_layout(self, name: str) -> QGridLayout:
        if not LayoutRegistry.contains(name):
            raise PieError(f"Can't find layout \"{name}\"")

        return LayoutRegistry.get(name)


def main(parent, plugin_path):
    return MainLayoutPlugin(parent, plugin_path)
