import typing

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QTableWidget, QAbstractItemView,
    QTableWidgetItem, QSizePolicy,
    QHeaderView, QLabel
)

from plugin.api import ContentTableAPI
from pieapp.structs.containers import Containers

from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class ContentTable(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    api = ContentTableAPI
    name = Containers.ContentTable

    def setColumns(self, count: int, columns: tuple = None) -> None:
        self.table.setColumnCount(count)
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(count)

    def setTextAlignment(self, count: int) -> None:
        headers = self.table.horizontalHeader()
        for column in range(count):
            headers.horizontalHeaderItem(column).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def setColumnsStretch(self, count: int) -> None:
        headers = self.table.horizontalHeader()
        for column in range(count):
            headers.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

    def fillTable(self, data: list[dict]) -> None:
        if not data:
            self.logger.error("No data were provided")
            return

        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(item))

        # We need to clear `tableLayout` to remove placeholder from it
        # But we don't need to do it in pyqt5... Yeah
        for item in reversed(range(self.parent().tableLayout.count())):
            self.parent().tableLayout.itemAt(item).widget().setParent(None)

        self.parent().tableLayout.addWidget(self.table, 1, 0)

    def setPlaceholder(self) -> None:
        placeholder = QLabel("<img src='{icon}' width=64 height=64><br>{text}".format(
            icon=self.getAsset("empty-box.png"),
            text=self.getTranslation("No files selected")
        ))
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parent().tableLayout.addWidget(placeholder, 1, 0)

    def init(self) -> None:
        self.table = QTableWidget()
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setPlaceholder()
        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )


def main(*args, **kwargs) -> typing.Any:
    return ContentTable(*args, **kwargs)
