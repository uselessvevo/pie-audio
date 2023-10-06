from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QListWidgetItem, QToolButton

from pieapp.structs.menus import MainMenu, MainMenuItem
from pieapp.structs.plugins import Plugin
from pieapp.structs.workbench import WorkbenchItem
from piekit.layouts.structs import Layout
from piekit.widgets.menus import INDEX_START

from piekit.globals import Global
from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from piekit.managers.plugins.decorators import on_plugin_event
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin

from api import ConverterAPI
from pieapp.structs.media import MediaFile

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
    sig_converter_table_ready = Signal()

    def init(self) -> None:
        self._converter_item_widgets: list[ConverterItemWidget] = []

        self._list_grid_layout = QGridLayout()
        self._main_layout = self.get_layout(Layout.Main)
        self._main_layout.add_layout(self._list_grid_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
        self._content_list = ConvertListWidget()
        self._set_placeholder()

    def _set_placeholder(self) -> None:
        self._pixmap_label = QLabel()
        self._pixmap_label.set_pixmap(QIcon(self.get_asset_icon("package.svg", section=self.name)).pixmap(100))
        self._pixmap_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._text_label = QLabel()
        self._text_label.set_text(self.get_translation("No files selected"))
        self._text_label.set_alignment(Qt.AlignmentFlag.AlignCenter)

        self._list_grid_layout.add_widget(self._pixmap_label, 1, 0)
        self._list_grid_layout.add_widget(self._text_label, 2, 0)

    def fill_list(self, media_files: list[MediaFile]) -> None:
        if not self._content_list.is_visible():
            self._list_grid_layout.remove_widget(self._pixmap_label)
            self._list_grid_layout.remove_widget(self._text_label)
            self._list_grid_layout.add_widget(self._content_list, 0, 0)

        for index, media_file in enumerate(media_files):
            widget = ConverterItemWidget(self._content_list, media_file)
            widget.set_title(media_file.info.filename)
            widget.set_description(f"{media_file.info.bit_rate}kb/s")
            widget.set_icon(media_file.info.codec.name)

            widget_layout = QHBoxLayout()
            widget_layout.add_stretch()
            widget_layout.add_widget(widget)

            item = QListWidgetItem()
            item.set_size_hint(widget.size_hint())

            self._content_list.add_item(item)
            self._content_list.set_item_widget(item, widget)

            self._converter_item_widgets.append(widget)

        self.sig_converter_table_ready.emit()

    def add_side_menu_item(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
    ) -> None:
        for item in self._converter_item_widgets:
            item.add_menu_item(name, text, icon, callback, before, after)

    @on_plugin_event(target=Plugin.MenuBar)
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

    @on_plugin_event(target=Plugin.Workbench)
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
