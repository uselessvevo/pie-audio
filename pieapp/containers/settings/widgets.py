from PySide6.QtGui import QAction
from __feature__ import snake_case
from pieapp.structs.containers import Container

from piekit.widgets.spacer import Spacer
from piekit.config.loader import Config
from piekit.utils.files import write_json
from piekit.managers.registry import Managers
from piekit.managers.structs import Section, SysManager
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor

from PySide6.QtCore import QDir

from PySide6.QtWidgets import (
    QWidget, QGridLayout,
    QLineEdit, QComboBox, QLabel, QFileDialog
)


class MainSettingsWidget(
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    QWidget
):
    name = Container.Settings
    section = Section.Shared

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        main_grid = QGridLayout(parent)

        self.ffmpeg_line_edit_action = QAction()
        self.ffmpeg_line_edit_action.set_icon(self.get_asset_icon("open-folder.png"))
        self.ffmpeg_line_edit_action.triggered.connect(self.ffmpeg_button_connect)

        self.ffmpeg_line_edit = QLineEdit()
        self.ffmpeg_line_edit.set_style_sheet("QLineEdit{font-size: 10pt;}")
        self.ffmpeg_line_edit.insert(self.get_shared_config("ffmpeg.root", section=Section.User))
        self.ffmpeg_line_edit.add_action(self.ffmpeg_line_edit_action, QLineEdit.ActionPosition.TrailingPosition)

        self._locales = Config.LOCALES
        self._cur_locale = self.get_shared_config("locales.locale", Config.DEFAULT_LOCALE, section=Section.User)
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self.locales_cbox = QComboBox()
        self.locales_cbox.set_style_sheet("QComboBox{font-size: 10pt;}")
        self.locales_cbox.insert_item(0, self._locales.pop(self._cur_locale))
        self.locales_cbox.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self.locales_cbox.currentIndexChanged.connect(self.locales_cbox_connect)

        themes = Managers(SysManager.Assets).get_themes()
        self.theme_cbox = QComboBox()
        self.theme_cbox.add_items(themes)
        self.theme_cbox.set_style_sheet("QComboBox{font-size: 10pt;}")
        self.theme_cbox.set_current_text(self.get_shared_config("assets.theme", section=Section.User))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        main_grid.add_widget(QLabel(self.get_translation("Language")), 0, 0, 1, 1)
        main_grid.add_widget(self.locales_cbox, 0, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("Theme")), 2, 0, 1, 1)
        main_grid.add_widget(self.theme_cbox, 2, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("FFmpeg path")), 6, 0, 1, 1)
        main_grid.add_widget(self.ffmpeg_line_edit, 6, 1, 1, 1)
        main_grid.add_widget(Spacer(), 7, 0, 1, 2)

        self.set_layout(main_grid)

    def theme_cbox_connect(self) -> None:
        new_theme = self.theme_cbox.current_text()
        self.set_config("assets.theme", {"theme": new_theme}, Section.User)

    def locales_cbox_connect(self) -> None:
        new_locale = self._locales_reversed.get(self.locales_cbox.current_text())
        self.set_config("locales.locale", {"locale": new_locale}, section=Section.User)
        # write_json(
        #     file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "locales.json"),
        #     data={"locale": new_locale},
        #     create=True
        # )

    def ffmpeg_button_connect(self) -> None:
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self,
            caption=self.get_translation("Select ffmpeg directory"),
            dir=str(Config.USER_ROOT)
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)

        if directory_path:
            self.set_config("ffmpeg.root", {"root": directory_path}, Section.User)
            # write_json(
            #     file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
            #     data={"root": directory_path},
            #     create=True
            # )
            # self.ffmpeg_line_edit.set_text(directory_path)
