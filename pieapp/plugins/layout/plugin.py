from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QVBoxLayout

from pieapp.api.plugins import PiePlugin
from pieapp.api.utils.qt import get_main_window
from pieapp.api.models.layouts import Layout
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.exceptions import PieError
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.layouts.registry import LayoutRegistry


class LayoutPlugin(PiePlugin):
    name = SysPlugin.Layout

    @staticmethod
    def get_name() -> str:
        return translate("Layout")

    @staticmethod
    def get_description() -> str:
        return translate("Layout manager")

    def init(self) -> None:
        self._root_layout = QVBoxLayout()
        self._root_layout.set_spacing(0)
        self._root_layout.set_contents_margins(0, 0, 0, 0)

        tools_layout = QHBoxLayout()

        workspace_layout = QGridLayout()
        ws_center_layout = QVBoxLayout()
        ws_right_layout = QVBoxLayout()
        ws_bottom_layout = QHBoxLayout()
        workspace_layout.add_layout(ws_center_layout, 0, 0)
        workspace_layout.add_layout(ws_right_layout, 0, 1)
        workspace_layout.add_layout(ws_bottom_layout, 1, 0, alignment=Qt.AlignmentFlag.AlignBottom)

        self._root_layout.add_layout(tools_layout)
        self._root_layout.add_layout(workspace_layout)

        self.add_layout(Layout.Tools, tools_layout)
        self.add_layout(Layout.Workspace, workspace_layout)
        self.add_layout(Layout.WorkspaceCenter, ws_center_layout, Layout.Workspace)
        self.add_layout(Layout.WorkspaceRight, ws_right_layout, Layout.Workspace)
        self.add_layout(Layout.WorkspaceBottom, ws_bottom_layout, Layout.Workspace)

        widget = QWidget()
        self.set_central_widget(widget)

    def set_central_widget(self, widget: "QWidget") -> None:
        main_window = get_main_window()
        widget.set_layout(self._root_layout)
        main_window.set_layout(self._root_layout)
        main_window.set_central_widget(widget)

    def add_layout(
        self,
        layout_name: str,
        layout: "QLayout",
        parent_layout_name: str = None
    ) -> None:
        """
        Args:
            layout_name (str): Name of the layout
            layout (Qt layout): Child layout object
            parent_layout_name (str): Parent layout name
        """
        if LayoutRegistry.contains(layout_name):
            raise PieError(f"Layout \"{parent_layout_name}\" already exists")

        LayoutRegistry.add(layout_name, layout, parent_layout_name)

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
    return LayoutPlugin(parent, plugin_path)
