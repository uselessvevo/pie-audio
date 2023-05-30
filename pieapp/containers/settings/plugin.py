from __feature__ import snake_case

import typing

from pieapp.structs.containers import Container
from pieapp.structs.menus import MainMenu, MainMenuItem

from piekit.plugins.plugins import PiePlugin
from piekit.widgets.tabbar import TabWidget
from piekit.managers.structs import Section
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.managers.plugins.decorators import on_plugin_available

from PySide6.QtWidgets import QGridLayout, QDialog

from .widgets import MainSettingsWidget


class Settings(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuAccessor,
    ToolBarAccessor,
    ToolButtonAccessor,
):
    name = Container.Settings
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"
    requires = [Container.MenuBar, Container.Workbench]

    def init(self) -> None:
        self.dialog = QDialog(self._parent)
        self.dialog.set_window_icon(self.get_plugin_icon())
        self.dialog.set_object_name("SettingsDialog")
        self.dialog.set_window_title(self.get_translation("Settings"))
        self.dialog.set_window_icon(self.get_plugin_icon())
        self.dialog.resize(740, 450)

        root_grid = QGridLayout(self.dialog)

        tab_widget = TabWidget(self.dialog)
        tab_widget.add_tab(MainSettingsWidget(), self.get_translation("Main"))

        root_grid.add_widget(tab_widget, 0, 0, 1, 2)
        self.dialog.set_layout(root_grid)

    @on_plugin_available(target=Container.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name="settings",
            text=self.get_translation("Settings"),
            triggered=self.dialog.show,
            icon=self.get_asset_icon("settings.png"),
            before=MainMenuItem.Exit
        )


def main(*args, **kwargs) -> typing.Any:
    return Settings(*args, **kwargs)
