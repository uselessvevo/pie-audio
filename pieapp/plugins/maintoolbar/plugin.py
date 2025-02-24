from __feature__ import snake_case

from PySide6.QtWidgets import QGridLayout

from layout.plugin import Layout
from pieapp.api.models.tabs import Tabs
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.tabs.mixins import TabBarAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin


class MainToolBar(PiePlugin, TabBarAccessorMixin, ToolBarAccessorMixin):
    name = SysPlugin.MainToolBar
    requires = [SysPlugin.ToolBarManager, SysPlugin.Layout]

    def init(self) -> None:
        self.toolbar = self.add_toolbar(self.name)

        self.tabs = self.add_tab(Tabs.Main, translate("Main"))
        self.tabs.set_movable(True)
        self.tabs.set_maximum_height(85)
        self.add_tab_item(Tabs.Main, self.name, self.toolbar)

        self.layout = QGridLayout()
        self.layout.set_column_stretch(0, 1)
        self.layout.set_row_stretch(0, 1)
        self.layout.set_row_minimum_height(0, 20)
        self.layout.add_widget(self.tabs)

    def on_plugins_ready(self) -> None:
        self.tabs.call()
        self.toolbar.call()

    @on_plugin_available(plugin=SysPlugin.Layout)
    def _on_layout_manager_available(self) -> None:
        layout_manager = get_plugin(SysPlugin.Layout)
        tools_layout = layout_manager.get_layout(Layout.Tools)
        if tools_layout:
            tools_layout.add_layout(self.layout)
            layout_manager.add_layout(self.name, tools_layout, Layout.Tools)


def main(parent, plugin_path):
    return MainToolBar(parent, plugin_path)
