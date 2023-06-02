from __feature__ import snake_case

import typing

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QGridLayout, QPushButton, QDialog

from pieapp.structs.menus import MainMenu
from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from pieapp.structs.plugins import Plugin
from pieapp.structs.containers import Container
from piekit.managers.menus.mixins import MenuAccessor

from piekit.config import Config
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.plugins.decorators import on_plugin_available


class About(
    PiePlugin,
    MenuAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Plugin.About
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"
    requires = [Container.MenuBar]

    def init(self) -> None:
        self.dialog = QDialog(self._parent)
        self.dialog.set_window_title(self.get_translation("About"))
        self.dialog.set_window_icon(self.get_plugin_icon())
        self.dialog.resize(400, 300)

        ok_button = QPushButton(self.get_translation("Ok"))
        ok_button.clicked.connect(self.dialog.close)

        pixmap = QPixmap()
        pixmap.load(self.get_asset("cloud.png"))

        icon_label = QLabel()
        icon_label.set_pixmap(pixmap)

        description_label = QLabel()
        description_label.set_text("Pie Audio • Audio Converter ({})".format(
            Config.PIEAPP_VERSION
        ))

        github_link_label = QLabel()
        github_link_label.set_open_external_links(True)
        github_link_label.set_text("<a href='https://github.com/uselessvevo/pie-audio/'>Project URL</a>")

        grid_layout = QGridLayout()
        grid_layout.add_widget(icon_label, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(description_label, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(github_link_label, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(ok_button, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.dialog.set_layout(grid_layout)

    @on_plugin_available(target=Container.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.Help,
            name="about",
            text=self.get_translation("About"),
            triggered=self.dialog.show,
            icon=self.get_asset_icon("help.png"),
        )


def main(*args, **kwargs) -> typing.Any:
    return About(*args, **kwargs)
