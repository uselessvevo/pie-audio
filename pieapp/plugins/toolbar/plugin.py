from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout, QSizePolicy

from pieapp.api.models.layouts import Layout
from pieapp.api.models.plugins import SysPlugin

from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin


class MainToolBar(PiePlugin, ToolBarAccessorMixin):
    name = SysPlugin.MainToolBar
    requires = [SysPlugin.Layout]

    def init(self) -> None:
        self._toolbar = self.add_toolbar(name=self.name)
        self._toolbar.set_object_name(self.name.capitalize())
        self._toolbar.set_floatable(True)
        self._toolbar.set_fixed_height(50)
        self._toolbar.set_contents_margins(6, 0, 10, 0)
        self._toolbar.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self._main_layout = QGridLayout()
        self._main_layout.add_widget(self._toolbar)

    def on_plugins_ready(self) -> None:
        self._toolbar.call()

    @on_plugin_available(plugin=SysPlugin.Layout)
    def _on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(SysPlugin.Layout)
        main_layout = layout_manager.get_layout(Layout.Main)
        if main_layout:
            layout_manager.add_layout(self.name, main_layout, self._main_layout, 0, 0, Qt.AlignmentFlag.AlignTop)


def main(parent: "QMainWindow", plugin_path: "Path"):
    return MainToolBar(parent, plugin_path)
