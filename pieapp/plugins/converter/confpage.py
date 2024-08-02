from __feature__ import snake_case

from pathlib import Path

from PySide6.QtGui import Qt
from PySide6.QtGui import QAction

from PySide6.QtCore import QDir
from PySide6.QtCore import Slot
from PySide6.QtCore import QThread

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QFormLayout

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.themes import ThemeProperties
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.converter.workers import DownloadWorker

from pieapp.api.registries.models import Scope
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class ConverterConfigPage(ConfigPage, ConfigAccessorMixin, ThemeAccessorMixin):
    name = SysPlugin.Converter

    def get_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", scope=self.name)

    def get_title(self) -> str:
        return translate("Converter")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        # Get config
        self._ffmpeg_root = Path(self.get_config("ffmpeg.root", Scope.User))

        self._main_widget = QWidget()
        self._main_widget.set_object_name("ConfigPageWidget")

        self._download_thread = QThread()
        self._download_worker = DownloadWorker()
        self._download_worker.sig_download_progress.connect(self._show_downloader_progress)
        self._download_worker.sig_download_done.connect(self._show_downloader_ready)
        self._download_worker.sig_unpack_archive_message.connect(self._download_worker_unpack)
        self._download_worker.sig_unpack_ready.connect(self._unpack_ready)
        self._download_worker.move_to_thread(self._download_thread)
        self._download_thread.started.connect(self._download_worker.start)
        self._download_thread.finished.connect(self._download_worker.delete_later)
        self._download_worker.destroyed.connect(self._download_worker.destroyed)

        self.line_edit_action = QAction()
        self.line_edit_action.set_icon(self.get_svg_icon("icons/folder-open.svg", prop=ThemeProperties.AppIconColor))
        # self.line_edit_action.set_icon(self._main_widget.style().standard_icon(QStyle.StandardPixmap.SP_DirIcon))
        self.line_edit_action.triggered.connect(self._select_ffmpeg_root_path)

        self._ffmpeg_line_edit = QLineEdit()
        self._ffmpeg_line_edit.set_placeholder_text(translate("Select ffmpeg directory or download latest release"))
        self._ffmpeg_line_edit.add_action(self.line_edit_action, QLineEdit.ActionPosition.TrailingPosition)

        if self._ffmpeg_root.exists():
            self._ffmpeg_line_edit.insert(str(self._ffmpeg_root))

        page_description = QLabel(translate(
            "Select directory with ffmpeg, "
            "ffprobe and ffplay or download its latest release"
        ))
        page_description.set_object_name("PageDescription")

        self._download_button = QPushButton()
        self._download_button.set_tool_tip(translate("Press me to download newest ffmpeg release"))
        self._download_button.set_maximum_width(self.get_theme_property("downloadButtonSize"))
        self._download_button.set_icon(self.get_svg_icon("icons/download.svg"))
        self._download_button.clicked.connect(self._start_downloader_thread)

        self._progress_bar = QProgressBar()
        self._progress_bar.set_format(f"{translate('Downloading files')}... (%p%/100%)")
        self._progress_bar.set_alignment(Qt.AlignmentFlag.AlignCenter)
        self._progress_bar.set_visible(False)

        ffmpeg_hbox = QHBoxLayout()
        ffmpeg_hbox.add_widget(self._download_button)
        ffmpeg_hbox.add_widget(self._ffmpeg_line_edit)

        layout = QVBoxLayout()
        layout.add_widget(page_description)
        layout.add_layout(ffmpeg_hbox)
        layout.add_widget(self._progress_bar)

        main_form_layout = QFormLayout()
        main_form_layout.add_row(layout)
        self._main_widget.set_layout(main_form_layout)

    def _start_downloader_thread(self) -> None:
        self.set_disabled(False)
        self._progress_bar.set_visible(True)
        self._ffmpeg_line_edit.set_disabled(True)
        self._download_button.set_disabled(True)
        self._download_thread.start(QThread.Priority.HighPriority)

    @Slot(int)
    def _show_downloader_progress(self, progress: int) -> None:
        self._progress_bar.set_value(progress)
        if round(progress, 0) >= 100:
            self._ffmpeg_line_edit.set_disabled(False)
            self._download_button.set_disabled(False)
            self._progress_bar.set_value(0)

    @Slot(str)
    def _show_downloader_ready(self, ffmpeg_path: str) -> None:
        self._progress_bar.set_format(translate("Done!"))
        self._ffmpeg_line_edit.set_focus()
        self._ffmpeg_line_edit.clear()
        self._ffmpeg_line_edit.insert(ffmpeg_path)

    @Slot(str)
    def _download_worker_unpack(self, status: str) -> None:
        self._progress_bar.set_format(status)

    @Slot(str)
    def _unpack_ready(self, ffmpeg_path: str) -> None:
        self.set_modified(True)
        self.set_disabled(False)
        self._progress_bar.set_visible(False)
        self._download_thread.terminate()

    def _select_ffmpeg_root_path(self) -> None:
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self._main_widget,
            caption=translate("Select ffmpeg directory"),
            dir=str(self._ffmpeg_root)
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)
        if directory_path:
            self.update_config("ffmpeg.root", Scope.User, directory_path)
            directory_path_obj = Path(directory_path)
            binaries = list(map(Path, ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe")))
            for binary in binaries:
                if not (directory_path_obj / binary).exists():
                    raise FileNotFoundError(
                        f"Binary file \"{binary.stem!s}\" not found. "
                        f"Please, download ffmpeg bundle from https://ffmpeg.org/download.html"
                    )

                self.update_config(f"ffmpeg.{binary.stem!s}", Scope.User, str(directory_path_obj / binary))

            self._ffmpeg_root = directory_path
            self._ffmpeg_line_edit.set_text(directory_path)
            self.set_modified(True)

    def accept(self) -> None:
        self.save_config(Scope.User)
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config(Scope.User)

    def set_page_state(self, disable: bool) -> None:
        self._ffmpeg_line_edit.set_disabled(disable)
        self._download_button.set_disabled(disable)
        self._progress_bar.set_disabled(disable)
