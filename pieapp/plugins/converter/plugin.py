from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QListWidgetItem

from pieapp.structs.menus import MainMenu, MainMenuItem
from pieapp.structs.plugins import Plugin
from pieapp.structs.workbench import WorkbenchItem
from piekit.layouts.structs import Layout
from piekit.widgets.menus import INDEX_START, INDEX_END

from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from piekit.managers.plugins.decorators import on_plugin_available
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin

from api import ConverterAPI
from models import MediaFile
from components.list import ConvertListWidget
from components.item import ConverterItemWidget


class Converter(
    PiePlugin, LayoutsAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin, AssetsAccessorMixin,
    MenuAccessorMixin, ToolBarAccessorMixin, ToolButtonAccessorMixin
):
    api = ConverterAPI
    name = Plugin.Converter
    requires = [Plugin.MenuBar, Plugin.Workbench]

    def init(self) -> None:
        self._list_grid_layout = QGridLayout()
        self._main_layout = self.get_layout(Layout.Main)
        self._main_layout.add_layout(self._list_grid_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
        self._content_list = ConvertListWidget()
        self.set_placeholder()

    def fill_list(self, files: list[MediaFile]) -> None:
        if not self._content_list.is_visible():
            widget = self._list_grid_layout.take_at(0)
            self._list_grid_layout.remove_item(widget)
            self._list_grid_layout.add_widget(self._content_list, 0, 0)

        for file in files:
            widget = ConverterItemWidget(self._content_list)
            widget.set_title(file.info.filename)
            widget.set_description(f"{file.info.bit_rate}kb/s")
            widget.set_icon(file.info.codec.name)

            widget_layout = QHBoxLayout()
            widget_layout.add_stretch()
            widget_layout.add_widget(widget)

            item = QListWidgetItem()
            item.set_size_hint(widget.size_hint())

            self._content_list.add_item(item)
            self._content_list.set_item_widget(item, widget)

    def set_placeholder(self) -> None:
        placeholder = QLabel("<img src='{icon}' width=64 height=64><br>{text}".format(
            icon=self.get_asset("empty-box.png"),
            text=self.get_translation("No files selected")
        ))
        placeholder.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._list_grid_layout.add_widget(placeholder, 1, 0)

    @on_plugin_available(target=Plugin.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.OpenFiles,
            text=self.get_translation("Open file"),
            icon=self.get_asset_icon("open-file.png"),
            index=INDEX_START(),
            triggered=self.api.open_files
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

    @on_plugin_available(target=Plugin.Workbench)
    def on_workbench_available(self) -> None:
        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.OpenFiles,
            text=self.get_translation("Open file"),
            tooltip=self.get_translation("Open file"),
            icon=self.get_asset_icon("open-folder.png"),
            triggered=self.api.open_files
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
            section=Plugin.Workbench,
            name=WorkbenchItem.Clear,
            item=self.get_tool_button(self.name, WorkbenchItem.Clear),
            before=WorkbenchItem.Spacer
        )

        self.add_toolbar_item(
            section=Plugin.Workbench,
            name=WorkbenchItem.Convert,
            item=self.get_tool_button(self.name, WorkbenchItem.Convert),
            before=WorkbenchItem.Spacer
        )

        self.add_toolbar_item(
            section=Plugin.Workbench,
            name=WorkbenchItem.OpenFiles,
            item=self.get_tool_button(self.name, WorkbenchItem.OpenFiles),
            before=WorkbenchItem.Spacer
        )


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return Converter(*args, **kwargs)
