from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy

from pieapp.api.plugins.decorators import on_plugin_event
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.structs.layouts import Layout
from pieapp.api.structs.plugins import Plugin
from pieapp.api.plugins.plugins import PiePlugin

from pieapp.api.managers.locales.mixins import LocalesAccessorMixin
from pieapp.api.managers.toolbars.mixins import ToolBarAccessorMixin


class MainToolBar(PiePlugin, LocalesAccessorMixin, ToolBarAccessorMixin):
    name = Plugin.MainToolBar
    requires = [Plugin.Layout]
    optional = [Plugin.MainMenuBar]

    def init(self) -> None:
        self._toolbar = self.add_toolbar(name=self.name)
        self._toolbar.set_fixed_height(50)
        self._toolbar.set_contents_margins(6, 0, 10, 0)
        self._toolbar.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self._workbench_layout = QGridLayout()
        self._workbench_layout.add_widget(self._toolbar)

    @on_plugin_event(target=Plugin.Layout)
    def on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(Plugin.Layout)
        layout = layout_manager.get_layout(Layout.Main)
        layout.add_layout(self._workbench_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout_manager.add_layout(self.name, self._workbench_layout)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MainToolBar(parent, plugin_path)
