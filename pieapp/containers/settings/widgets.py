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

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QPushButton, 
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

        self.ffpeg_prompt = QLineEdit()
        self.ffpeg_prompt.insert(self.get_shared_config("ffmpeg.root", section=Section.User))
        self.ffmpeg_button = QPushButton(self.get_translation("Set ffmpeg path"))
        self.ffmpeg_button.clicked.connect(self.ffmpeg_button_connect)

        locales = Config.LOCALES
        self.locales_cbox = QComboBox()
        self.locales_cbox.add_items(locales)
        self.locales_cbox.set_current_text(self.get_shared_config(
            "locales.locale", Config.DEFAULT_LOCALE, section=Section.User
        ))

        themes = Managers(SysManager.Assets).get_themes()
        self.theme_cbox = QComboBox()
        self.theme_cbox.add_items(themes)
        self.theme_cbox.set_current_text(self.get_shared_config("assets.theme", section=Section.User))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        main_grid.add_widget(QLabel(self.get_translation("Language")), 0, 0, 1, 1)
        main_grid.add_widget(self.locales_cbox, 0, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("Theme")), 2, 0, 1, 1)
        main_grid.add_widget(self.theme_cbox, 2, 1, 1, 1)

        main_grid.add_widget(QLabel(self.get_translation("FFmpeg path")), 6, 0, 1, 1)
        main_grid.add_widget(self.ffpeg_prompt, 6, 1, 1, 1)
        main_grid.add_widget(self.ffmpeg_button, 7, 1, 1, 1)
        main_grid.set_alignment(self.ffmpeg_button, Qt.AlignmentFlag.AlignRight)
        main_grid.add_widget(Spacer(), 8, 0, 1, 2)

        self.set_layout(main_grid)

    def ffmpeg_button_connect(self) -> None:
        directory = QFileDialog(self, self.get_translation("Select ffmpeg directory"))
        directory.set_file_mode(QFileDialog.FileMode.Directory)
        directory.set_option(QFileDialog.Option.ShowDirsOnly, False)
        directory.get_existing_directory(self, dir=str(Config.USER_ROOT))
        directory_path = directory.directory().path()

        if directory_path:
            write_json(
                file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
                data={"root": directory_path},
                create=True
            )
            self.ffpeg_prompt.set_text(directory_path)
