from __feature__ import snake_case

from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QGridLayout, QListWidget

from pieapp.structs.plugins import Plugin
from piekit.layouts.structs import Layout
from piekit.managers.layouts.mixins import LayoutsAccessorMixin

from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from api import ContentTableAPI
from components.item import ContentTableItem


class ContentTable(
    PiePlugin, LayoutsAccessorMixin,
    ConfigAccessorMixin, LocalesAccessorMixin, AssetsAccessorMixin,
):
    api = ContentTableAPI
    name = Plugin.ContentTable

    def init(self) -> None:
        self._list_grid_layout = QGridLayout()
        self._main_layout = self.get_layout(Layout.Main)
        self._main_layout.add_layout(self._list_grid_layout, 1, 0, Qt.AlignmentFlag.AlignTop)
        self._content_list = QListWidget()

    def fill_list(self, items: list[MediaFileModel]) -> None:
        if self._content_list.is_visible():
            self._list_grid_layout.add_widget(self._content_list, 0, 0)

        # self._content_list.itemDoubleClicked.connect()
        for item in items:
            title = f"{item}"

    def set_placeholder(self) -> None:
        placeholder = QLabel("<img src='{icon}' width=64 height=64><br>{text}".format(
            icon=self.get_asset("empty-box.png"),
            text=self.get_translation("No files selected")
        ))
        placeholder.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._list_grid_layout.add_widget(placeholder, 1, 0)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    return ContentTable(*args, **kwargs)
