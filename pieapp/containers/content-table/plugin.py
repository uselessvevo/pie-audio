from __feature__ import snake_case

import typing

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, 
    QSizePolicy, QHeaderView, QLabel
)

from pieapp.structs.containers import Container

from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor

from .api import ContentTableAPI


class ContentTable(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    api = ContentTableAPI
    name = Container.ContentTable
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"

    def set_columns(self, count: int, columns: tuple = None) -> None:
        self.table.set_column_count(count)
        self.table.set_horizontal_header_labels(columns)
        self.table.set_row_count(count)

    def set_text_alignment(self, count: int) -> None:
        headers = self.table.horizontal_header()
        for column in range(count):
            headers.horizontal_header_item(column).set_text_alignment(Qt.AlignmentFlag.AlignCenter)

    def set_columns_stretch(self, count: int) -> None:
        headers = self.table.horizontal_header()
        for column in range(count):
            headers.set_section_resize_mode(column, QHeaderView.ResizeMode.Stretch)

    def fill_table(self, data: list[dict]) -> None:
        if not data:
            self.logger.error("No data were provided")
            return

        for row, item in enumerate(data):
            self.table.set_item(row, 0, QTableWidgetItem(item))

        # We need to clear `table_layout` to remove placeholder from it
        # But we don't need to do it in pyqt5... Yeah
        for item in reversed(range(self._parent.table_layout.count())):
            self._parent.table_layout.item_at(item).widget().set_parent(None)

        self._parent.table_layout.add_widget(self.table, 1, 0)

    def set_placeholder(self) -> None:
        placeholder = QLabel("<img src='{icon}' width=64 height=64><br>{text}".format(
            icon=self.get_asset("empty-box.png"),
            text=self.get_translation("No files selected")
        ))
        placeholder.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._parent.table_layout.add_widget(placeholder, 1, 0)

    def init(self) -> None:
        self.table = QTableWidget()
        # self.table.set_selection_model(QAbstractItemView.SelectionMode.NoSelection)
        self.set_placeholder()
        self.table.set_size_policy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )


def main(*args, **kwargs) -> typing.Any:
    return ContentTable(*args, **kwargs)
