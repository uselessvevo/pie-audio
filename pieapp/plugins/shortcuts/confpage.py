from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QTableWidgetItem
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QGridLayout

from pieapp.api.registries.models import Scope
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.shortcuts.manager import Shortcuts
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from pieapp.api.plugins import ConfigPage
from pieapp.api.models.plugins import SysPlugin
from pieapp.widgets.delegates import ReadOnlyDelegate


class ShortcutBlankConfigPage(ConfigPage, ThemeAccessorMixin):
    name = SysPlugin.ShortcutBlank
    scope = Scope.Root

    def get_icon(self) -> Union[QIcon, None]:
        return self.get_svg_icon("icons/hourglass.svg")

    def get_title(self) -> str:
        return f'{translate("Shortcuts")} ({translate("Loading")}...)'

    def init(self) -> None:
        self._main_widget = QWidget()
        grid_layout = QGridLayout()
        blank_label = QLabel(translate("Loading..."))
        grid_layout.add_widget(blank_label)
        self._main_widget.set_layout(grid_layout)

    def get_page_widget(self) -> QWidget:
        return self._main_widget


class ShortcutConfigPage(
    ConfigPage,
    ConfigAccessorMixin,
    ThemeAccessorMixin,
):
    name = SysPlugin.Shortcut
    scope = Scope.Root

    def get_icon(self) -> QIcon:
        return self.get_svg_icon("icons/keyboard.svg")

    def get_title(self) -> str:
        return translate("Shortcuts")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        self._main_widget = QWidget()
        self._main_widget.set_object_name("ConfigPageWidget")
        grid_layout = QGridLayout()

        table_widget = QTableWidget()
        table_widget.set_object_name("ShortcutsTable")
        table_widget.set_row_count(15)
        table_widget.set_column_count(3)
        table_widget.vertical_header().hide()
        table_widget.horizontal_header().hide()
        table_widget.horizontal_header().set_section_resize_mode(0, QHeaderView.ResizeMode.ResizeToContents)
        table_widget.horizontal_header().set_section_resize_mode(1, QHeaderView.ResizeMode.ResizeToContents)
        table_widget.horizontal_header().set_section_resize_mode(2, QHeaderView.ResizeMode.ResizeToContents)
        table_widget.set_item_delegate_for_column(0, ReadOnlyDelegate(self._main_widget))

        table_widget.set_item(0, 0, QTableWidgetItem(translate(translate("Name"))))
        table_widget.set_item(0, 1, QTableWidgetItem(translate(translate("Description"))))
        table_widget.set_item(0, 2, QTableWidgetItem(translate(translate("Shortcut key"))))

        registry_values = list(filter(lambda v: v["hidden"] is False, Shortcuts.values()))
        for row, data in enumerate(registry_values, 1):
            table_widget.set_item(row, 0, QTableWidgetItem(data["title"]))
            table_widget.set_item(row, 1, QTableWidgetItem(data["description"]))
            table_widget.set_item(row, 2, QTableWidgetItem(data["shortcut_key"]))

        page_description = QLabel(translate("Customize application shortcuts"))
        page_description.set_object_name("PageDescription")

        grid_layout.add_widget(page_description, 0, 0)
        grid_layout.add_widget(table_widget, 1, 0)
        self._main_widget.set_layout(grid_layout)
