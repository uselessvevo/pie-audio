import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView

from pieapp.structs.containers import Containers
from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class ContentTable(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Containers.ContentTable

    def init(self) -> None:
        employees = [
            {'First Name': 'John', 'Last Name': 'Doe', 'Age': 25},
            {'First Name': 'Jane', 'Last Name': 'Doe', 'Age': 22},
            {'First Name': 'Alice', 'Last Name': 'Doe', 'Age': 22},
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(employees[0].keys())
        self.table.setRowCount(len(employees))

        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)

        headers = self.table.horizontalHeader()
        headers.setSectionResizeMode(0, QHeaderView.Stretch)
        headers.setSectionResizeMode(1, QHeaderView.Stretch)
        headers.setSectionResizeMode(2, QHeaderView.Stretch)

        for row, e in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(e['First Name']))
            self.table.setItem(row, 1, QTableWidgetItem(e['Last Name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(e['Age'])))

        self.parent().contentLayout.addWidget(self.table)


def main(*args, **kwargs) -> typing.Any:
    return ContentTable(*args, **kwargs)
