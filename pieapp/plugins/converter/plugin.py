from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QListWidgetItem

from pieapp.structs.menus import MainMenu, MainMenuItem
from pieapp.structs.plugins import Plugin
from pieapp.structs.workbench import WorkbenchItem
from piekit.layouts.structs import Layout
from piekit.widgets.menus import INDEX_START, INDEX_END

from piekit.globals import Global
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

    def set_placeholder(self) -> None:
        pixmap_label = QLabel()
        pixmap_label.set_pixmap(QIcon(self.get_asset_icon("package.svg", section=self.name)).pixmap(100))
        pixmap_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel()
        text_label.set_text(self.get_translation("No files selected"))
        text_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._list_grid_layout.add_widget(pixmap_label, 1, 0)
        self._list_grid_layout.add_widget(text_label, 2, 0)

    def fill_list(self, files: list[MediaFile]) -> None:
        if not self._content_list.is_visible():
            widget = self._list_grid_layout.take_at(0)
            self._list_grid_layout.remove_item(widget)
            self._list_grid_layout.add_widget(self._content_list, 0, 0)

        for index, file in enumerate(files):
            widget = ConverterItemWidget(self._content_list, index, file.info.codec.name)
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

    @on_plugin_available(target=Plugin.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.OpenFiles,
            text=self.get_translation("Open file"),
            icon=self.get_svg_icon("folder-open.svg"),
            index=INDEX_START(),
            triggered=self.api.open_files
        )

        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.File,
            name=MainMenuItem.Exit,
            text=self.get_translation("Exit"),
            icon=self.get_svg_icon("logout.svg"),
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
            icon=self.get_svg_icon("folder-open.svg"),
            triggered=self.api.open_files,
            object_name="WorkbenchToolButton"
        )

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Convert,
            text=self.get_translation("Convert"),
            tooltip=self.get_translation("Convert"),
            icon=self.get_svg_icon("bolt.svg"),
            object_name="WorkbenchToolButton"
        ).set_enabled(False)

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Clear,
            text=self.get_translation("Clear"),
            tooltip=self.get_translation("Clear"),
            icon=self.get_svg_icon("delete.svg"),
            object_name="WorkbenchToolButton"
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


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    Global.load_by_path(str(plugin_path / "globals.py"))
    return Converter(parent, plugin_path)
