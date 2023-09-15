from typing import Union

from __feature__ import snake_case

from piekit.widgets.spacer import Spacer
from piekit.globals.loader import Global
from piekit.managers.registry import Managers
from piekit.managers.structs import Section, SysManager
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from piekit.managers.confpages.structs import ConfigPage

from PySide6.QtCore import QDir
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QGridLayout,
    QLineEdit, QComboBox, QLabel, QFileDialog
)


class AppConfigPage(
    ConfigAccessorMixin,
    LocalesAccessorMixin,
    AssetsAccessorMixin,
    ConfigPage
):
    name = Section.Root
    section = Section.Root

    def init(self) -> None:
        # TODO: Replace all the layouts with the QFormLayout yeah
        self._main_widget = QWidget()
        main_grid = QGridLayout()

        self._ffmpeg_line_edit_action = QAction()
        self._ffmpeg_line_edit_action.set_icon(self.get_asset_icon("open-folder.png"))
        self._ffmpeg_line_edit_action.triggered.connect(self._ffmpeg_button_connect)

        self._ffmpeg_line_edit = QLineEdit()
        self._ffmpeg_line_edit.set_object_name("SettingsLineEdit")
        self._ffmpeg_line_edit.insert(
            self.get_config("ffmpeg.root", scope=Section.Root, section=Section.User)
        )
        self._ffmpeg_line_edit.add_action(
            self._ffmpeg_line_edit_action, QLineEdit.ActionPosition.TrailingPosition
        )

        self._locales = Global.LOCALES
        self._cur_locale = self.get_config(
            key="locale.locale",
            default=Global.DEFAULT_LOCALE,
            scope=Section.Root,
            section=Section.User
        )
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self._locales_cbox = QComboBox()
        self._locales_cbox.set_object_name("SettingsComboBox")
        self._locales_cbox.insert_item(0, self._locales.pop(self._cur_locale))
        self._locales_cbox.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self._locales_cbox.currentIndexChanged.connect(self._locales_cbox_connect)

        themes = Managers(SysManager.Assets).get_themes()
        self._theme_cbox = QComboBox()
        self._theme_cbox.add_items(themes)
        self._theme_cbox.set_current_text(self.get_config(
            "assets.theme", scope=Section.Root, section=Section.User
        ))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        main_grid.add_widget(QLabel(self.get_translation("Language")), 0, 0, 1, 1)
        main_grid.add_widget(self._locales_cbox, 0, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("Theme")), 2, 0, 1, 1)
        main_grid.add_widget(self._theme_cbox, 2, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("FFmpeg path")), 6, 0, 1, 1)
        main_grid.add_widget(self._ffmpeg_line_edit, 6, 1, 1, 1)
        main_grid.add_widget(Spacer(), 7, 0, 1, 2)

        self._main_widget.set_layout(main_grid)

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def _theme_cbox_connect(self) -> None:
        new_theme = self._theme_cbox.current_text()
        self.set_config("assets.theme", new_theme, section=Section.User, temp=True)
        self.set_modified(True)

    def _locales_cbox_connect(self) -> None:
        new_locale = self._locales_reversed.get(self._locales_cbox.current_text())
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="locale.locale",
            data=new_locale,
            temp=True
        )
        self.set_modified(True)

    def _ffmpeg_button_connect(self) -> None:
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self._main_widget,
            caption=self.get_translation("Select ffmpeg directory"),
            dir=str(Global.USER_ROOT)
        )

        directory_path = QDir.to_native_separators(ffmpeg_directory)
        if directory_path:
            self.set_config("ffmpeg.path", directory_path, section=Section.User, temp=True)

        self.set_modified(True)

    def accept(self) -> None:
        self.save_config(scope=Section.Root, section=Section.User, temp=True)
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config()

    def get_title(self) -> str:
        return self.get_translation("Main")

    def get_icon(self) -> Union[QIcon, None]:
        return self.get_asset_icon("cloud.png")


def main(*args, **kwargs) -> Union[ConfigPage, None]:
    return AppConfigPage(*args, **kwargs)
