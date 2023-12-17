import os
from pathlib import Path

from __feature__ import snake_case

from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton, QLabel

from pieapp.structs.plugins import Plugin

from piekit.globals import Global
from piekit.widgets.collapse import Collapsable
from piekit.plugins.confpage import ConfigPage
from piekit.managers.structs import Section
from piekit.managers.locales.helpers import translate
from piekit.managers.themes.mixins import ThemeAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin


class ConverterConfigPage(
    ConfigPage,
    ConfigAccessorMixin,
    LocalesAccessorMixin,
    ThemeAccessorMixin
):
    name = Plugin.Converter

    def get_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", section=self.name)

    def get_title(self) -> str:
        return self.translate("Converter")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        self._main_widget = QWidget()
        main_form_layout = QFormLayout()

        self._ffmpeg_line_edit_action = QAction()
        self._ffmpeg_line_edit_action.set_icon(self.get_svg_icon("icons/folder.svg"))
        self._ffmpeg_line_edit_action.triggered.connect(self._ffmpeg_button_connect)

        self._ffmpeg_line_edit = QLineEdit()
        self._ffmpeg_line_edit.set_object_name("PreferencesLineEdit")
        self._ffmpeg_line_edit.insert(self.get_config(
            "ffmpeg.root", scope=Section.Root, section=Section.User
        ))
        self._ffmpeg_line_edit.add_action(
            self._ffmpeg_line_edit_action,
            QLineEdit.ActionPosition.TrailingPosition
        )

        # Setup `Collapsable` widget
        collapsable = Collapsable("Setup via environment variables", 0, self._main_widget)
        collapsable.set_object_name("ConverterPreferencesCollapsable")

        self._ffmpeg_env_line_edit = QLineEdit(collapsable)
        self._ffprobe_env_line_edit = QLineEdit(collapsable)
        self._ffplay_env_line_edit = QLineEdit(collapsable)

        self._ffmpeg_env_line_edit.set_placeholder_text(translate("Alias for ffmpeg"))
        self._ffmpeg_env_line_edit.textChanged.connect(self._ffmpeg_env_line_edit_changed)
        self._ffmpeg_env_line_edit.insert(self.get_config(
            key="ffmpeg.ffmpeg_env",
            default="ffmpeg",
            scope=Section.Root,
            section=Section.User
        ))

        self._ffprobe_env_line_edit.set_placeholder_text(translate("Alias for ffprobe"))
        self._ffprobe_env_line_edit.textChanged.connect(self._ffprobe_env_line_edit_changed)
        self._ffprobe_env_line_edit.insert(self.get_config(
            key="ffmpeg.ffprobe_env",
            default="ffprobe",
            scope=Section.Root,
            section=Section.User
        ))

        self._ffplay_env_line_edit.set_placeholder_text(translate("Alias for ffplay"))
        self._ffplay_env_line_edit.textChanged.connect(self._ffplay_env_line_edit_changed)
        self._ffplay_env_line_edit.insert(self.get_config(
            key="ffmpeg.ffplay_env",
            default="ffplay",
            scope=Section.Root,
            section=Section.User
        ))

        collapsable_vbox_layout = QVBoxLayout()
        collapsable_vbox_layout.add_widget(self._ffmpeg_env_line_edit)
        collapsable_vbox_layout.add_widget(self._ffprobe_env_line_edit)
        collapsable_vbox_layout.add_widget(self._ffplay_env_line_edit)
        collapsable.set_content_layout(collapsable_vbox_layout)

        main_form_layout.add_row(translate("Converter binaries path"), self._ffmpeg_line_edit)
        main_form_layout.add_row(collapsable)
        self._main_widget.set_layout(main_form_layout)

    def _ffmpeg_env_line_edit_changed(self) -> None:
        self.set_config(
            key="ffmpeg.ffmpeg_env",
            data=self._ffmpeg_env_line_edit.text(),
            scope=Section.Root,
            section=Section.User,

        )
        self.set_modified(True)

    def _ffprobe_env_line_edit_changed(self) -> None:
        self.set_config(
            key="ffmpeg.ffprobe_env",
            data=self._ffprobe_env_line_edit.text(),
            scope=Section.Root,
            section=Section.User,

        )
        self.set_modified(True)

    def _ffplay_env_line_edit_changed(self) -> None:
        self.set_config(
            key="ffmpeg.ffplay_env",
            data=self._ffplay_env_line_edit.text(),
            scope=Section.Root,
            section=Section.User,

        )
        self.set_modified(True)

    def _ffmpeg_button_connect(self) -> None:
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self._main_widget,
            caption=self.translate("Select ffmpeg directory"),
            dir=self.get_config(
                key="ffmpeg.root",
                default=Global.USER_ROOT,
                scope=Section.Root,
                section=Section.User,
            )
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)

        if directory_path:
            self.set_config(
                scope=Section.Root,
                section=Section.User,
                key="ffmpeg.root",
                data=directory_path,
            )
            directory_path_obj = Path(directory_path)
            binaries = list(map(Path, ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe")))
            for binary in binaries:
                if not (directory_path_obj / binary).exists():
                    raise FileNotFoundError(
                        f"Binary file \"{binary.stem!s}\" not found. "
                        f"Please, download ffmpeg bundle from https://ffmpeg.org/download.html"
                    )

                self.set_config(
                    scope=Section.Root,
                    section=Section.User,
                    key=f"ffmpeg.{binary.stem!s}",
                    data=str(directory_path_obj / binary),
                )

            self._ffmpeg_path = directory_path
            self._ffmpeg_line_edit.set_text(directory_path)
            self.set_modified(True)

    def accept(self) -> None:
        self.save_config(scope=Section.Root, section=Section.User)
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config()
