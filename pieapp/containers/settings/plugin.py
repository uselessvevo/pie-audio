from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel

from pieapp.structs.containers import Container
from pieapp.structs.menus import MainMenu, MainMenuItem
from piekit.managers.confpages.structs import ConfigurationPage

from piekit.plugins.plugins import PiePlugin
from piekit.managers.structs import Section
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.managers.plugins.decorators import on_plugin_available

from PySide6.QtWidgets import QGridLayout, QDialog, QTreeView


class Settings(
    PiePlugin,
    ConfigAccessor, LocalesAccessor, AssetsAccessor,
    MenuAccessor, ToolBarAccessor, ToolButtonAccessor,
):
    name = Container.Settings
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"
    requires = [Container.MenuBar, Container.Workbench]

    def init(self) -> None:
        # Setup treeview
        self._treeview_model = QStandardItemModel(0, 3, self.parent())
        self._treeview_model.set_header_data(0, Qt.Orientation.Horizontal, self.get_translation("Settings"))
        self._treeview_model.insert_row(0)
        # self._treeview_model.set_data(self._treeview_model.index(0, 0), "")

        self._treeview_widget = QTreeView()
        self._treeview_widget.set_model(self._treeview_model)
        self._treeview_widget.set_header_hidden(True)

        self._dialog = QDialog(self._parent)
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.set_object_name("SettingsDialog")
        self._dialog.set_window_title(self.get_translation("Settings"))
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(740, 450)

        self._root_grid = QGridLayout(self._dialog)
        self._root_grid.add_widget(self._treeview_widget, 0, 0, 1, 2)

        self._dialog.set_layout(self._root_grid)

    def call(self) -> None:
        self._dialog.show()

    @on_plugin_available(target=Container.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name="settings",
            text=self.get_translation("Settings"),
            triggered=self.call,
            icon=self.get_plugin_icon(),
            before=MainMenuItem.Exit
        )


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return Settings(*args, **kwargs)
