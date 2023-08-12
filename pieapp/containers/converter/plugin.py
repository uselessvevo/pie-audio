from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QDialog, QFileDialog

from pieapp.structs.menus import MainMenu, MainMenuItem
from piekit.managers.structs import Section
from piekit.plugins.api.utils import get_api
from piekit.plugins.plugins import PiePlugin
from pieapp.structs.plugins import Plugin
from pieapp.structs.containers import Container
from piekit.managers.menus.mixins import MenuAccessorMixin

from pieapp.structs.workbench import WorkbenchItem
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_available
from piekit.widgets.menus import INDEX_END, INDEX_START


class Converter(
    PiePlugin,
    MenuAccessorMixin,
    LocalesAccessorMixin,
    AssetsAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin
):
    name = Plugin.Converter
    requires = [Container.Workbench, Container.MenuBar]

    def init(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_window_title(self.get_translation("Convert"))
        self._dialog.set_window_icon(self.get_asset_icon("go.png"))
        self._dialog.resize(400, 300)

    def open_files(self) -> None:
        file_dialog = QFileDialog(self._dialog, self.get_translation("Open files"))
        selected_files = file_dialog.get_open_file_names(self._dialog)
        get_api(Container.ContentTable, method="receive", files=selected_files[0])

    @on_plugin_available(target=Container.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.menu_bar = self.get_menu_bar(Section.Shared)

        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.OpenFiles,
            text=self.get_translation("Open file"),
            icon=self.get_asset_icon("open-file.png"),
            index=INDEX_START(),
            triggered=self.open_files
        )

        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=self.get_translation("Exit"),
            icon=self.get_asset_icon("exit.png"),
            triggered=self._parent.close,
            index=INDEX_END()
        )

    @on_plugin_available(target=Container.Workbench)
    def on_workbench_available(self) -> None:
        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.OpenFiles,
            text=self.get_translation("Open file"),
            tooltip=self.get_translation("Open file"),
            icon=self.get_asset_icon("open-folder.png"),
            triggered=self.open_files
        )

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Convert,
            text=self.get_translation("Convert"),
            tooltip=self.get_translation("Convert"),
            icon=self.get_asset_icon("go.png")
        ).set_enabled(False)

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Clear,
            text=self.get_translation("Clear"),
            tooltip=self.get_translation("Clear"),
            icon=self.get_asset_icon("recycle-bin.png")
        ).set_enabled(False)

        self.add_toolbar_item(
            section=Container.Workbench,
            name=WorkbenchItem.Clear,
            item=self.get_tool_button(self.name, WorkbenchItem.Clear),
            before=WorkbenchItem.Spacer
        )

        self.add_toolbar_item(
            section=Container.Workbench,
            name=WorkbenchItem.Convert,
            item=self.get_tool_button(self.name, WorkbenchItem.Convert),
            before=WorkbenchItem.Spacer
        )

        self.add_toolbar_item(
            section=Container.Workbench,
            name=WorkbenchItem.OpenFiles,
            item=self.get_tool_button(self.name, WorkbenchItem.OpenFiles),
            before=WorkbenchItem.Spacer
        )


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return Converter(*args, **kwargs)
