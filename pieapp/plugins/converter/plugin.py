from typing import Union, Generator

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QListWidgetItem, QToolButton, QAbstractItemView

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

from components.list import ConverterListWidget
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

        # Setup grid layouts
        self._list_grid_layout = QGridLayout()
        self._main_layout = self.get_layout(Layout.Main)
        self._main_layout.add_layout(self._list_grid_layout, 1, 0, Qt.AlignmentFlag.AlignTop)

        # Setup content list
        self._content_list = ConverterListWidget()
        self._content_list.set_focus_policy(Qt.FocusPolicy.NoFocus)
        self._content_list.set_selection_behavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._content_list.set_selection_mode(QAbstractItemView.SelectionMode.SingleSelection)

        # Setup placeholder
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

    def _clear_content_list(self) -> None:
        self._converter_item_widgets = []
        self._content_list.clear()
        self._content_list.set_visible(False)
        self._list_grid_layout.remove_widget(self._content_list)
        self._set_placeholder()
        self.api.clear_files()

        for item in self._converter_item_widgets:
            del item

    def _delete_tool_button_connect(self, media_file: MediaFile) -> None:
        selected_index = self._content_list.selected_indexes()[0]
        self._content_list.take_item(selected_index.row())
        del self._converter_item_widgets[selected_index.row()]

    def fill_list(self, media_files: list[MediaFile]) -> None:
        if not media_files:
            return

        if not self._content_list.is_visible():
            self._list_grid_layout.remove_widget(self._pixmap_label)
            self._list_grid_layout.remove_widget(self._text_label)
            self._list_grid_layout.add_widget(self._content_list, 0, 0)

        for index, media_file in enumerate(media_files):
            widget = ConverterItemWidget(self._content_list, media_file)
            widget.set_title(media_file.info.filename)
            widget.set_description(f"{media_file.info.bit_rate}kb/s")
            widget.set_icon(media_file.info.codec.name)

            widget.add_quick_action(
                name="delete",
                text=self.get_translation("Delete"),
                icon=self.get_svg_icon("delete.svg"),
                callback=self._delete_tool_button_connect
            )

            widget_layout = QHBoxLayout()
            widget_layout.add_stretch()
            widget_layout.add_widget(widget)

            item = QListWidgetItem()
            item.set_size_hint(widget.size_hint())

            # A really nasty hack to get item `row` inside `QWidgetItem`
            widget.set_list_widget(item)

            self._content_list.add_item(item)
            self._content_list.set_item_widget(item, widget)

            self._converter_item_widgets.append(widget)

        clear_button = self.get_tool_button(self.name, WorkbenchItem.Clear)
        if clear_button:
            clear_button.set_disabled(False)

        self.sig_converter_table_ready.emit()

    def disable_side_menu_items(self) -> None:
        for item in self._converter_item_widgets:
            item.set_items_disabled()

    def add_quick_action(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
    ) -> None:
        for item in self._converter_item_widgets:
            item.add_quick_action(name, text, icon, callback, before, after)

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
            triggered=self.api.open_files
        )

        self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Convert,
            text=self.get_translation("Convert"),
            tooltip=self.get_translation("Convert"),
            icon=self.get_svg_icon("bolt.svg")
        ).set_enabled(False)

        clear_tool_button = self.add_tool_button(
            section=self.name,
            name=WorkbenchItem.Clear,
            text=self.get_translation("Clear"),
            tooltip=self.get_translation("Clear"),
            icon=self.get_svg_icon("delete.svg")
        )
        clear_tool_button.set_enabled(False)
        clear_tool_button.clicked.connect(self._clear_content_list)

        self.add_toolbar_item(
            section=Plugin.Workbench,
            name=WorkbenchItem.OpenFiles,
            item=self.get_tool_button(self.name, WorkbenchItem.OpenFiles),
        )

        self.add_toolbar_item(
            section=Plugin.Workbench,
            name=WorkbenchItem.Convert,
            item=self.get_tool_button(self.name, WorkbenchItem.Convert),
            after=WorkbenchItem.OpenFiles
        )

        self.add_toolbar_item(
            section=Plugin.Workbench,
            name=WorkbenchItem.Clear,
            item=self.get_tool_button(self.name, WorkbenchItem.Clear),
            after=WorkbenchItem.Convert
        )


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    Global.load_by_path(str(plugin_path / "globals.py"))
    return Converter(parent, plugin_path)
