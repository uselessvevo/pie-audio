from __feature__ import snake_case
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QDir
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QFileDialog
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor

from piekit.managers.structs import SysManager, Section
from piekit.utils.files import write_json
from piekit.utils.core import restart_application

from piekit.managers.registry import Managers
from piekit.config import Config


class LocaleWizardPage(
    ConfigAccessor,
    LocalesAccessor,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self._locales = Config.LOCALES
        self._cur_locale = self.get_shared_config("locales.locale", Config.DEFAULT_LOCALE, Section.User)
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 12pt;}")
        self.combo_box.insert_item(0, self._locales.pop(self._cur_locale))
        self.combo_box.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self.combo_box.currentIndexChanged.connect(self.get_result)

        self.locale_label = QtWidgets.QLabel(self.get_translation("Select locale"))
        self.locale_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(self.locale_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def get_result(self):
        new_locale = self._locales_reversed.get(self.combo_box.current_text())
        write_json(
            file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "locales.json"),
            data={"locale": new_locale},
            create=True
        )

        if self._cur_locale != new_locale:
            restart_application()

        return new_locale


class ThemeWizardPage(
    ConfigAccessor,
    LocalesAccessor,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 12pt;}")
        self.combo_box.add_items(Managers(SysManager.Assets).get_themes())
        self.combo_box.currentIndexChanged.connect(self.get_result)

        self._cur_theme = self.get_shared_config("assets.theme", Managers(SysManager.Assets).get_theme(), Section.User)

        theme_label = QtWidgets.QLabel(self.get_translation("Select theme"))
        theme_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(theme_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def get_result(self):
        new_theme = self.combo_box.current_text()
        write_json(
            file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "assets.json"),
            data={"theme": new_theme},
            create=True
        )

        if self._cur_theme != new_theme:
            restart_application()

        return self.combo_box.current_text()


class FfmpegWizardPage(
    LocalesAccessor,
    AssetsAccessor,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self.ffmpeg_path = None

        self.line_edit_action = QAction()
        self.line_edit_action.set_icon(self.get_asset_icon("open-folder.png"))
        self.line_edit_action.triggered.connect(self.select_ffmpeg_path)

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.set_style_sheet("QLineEdit{font-size: 15pt;}")
        self.line_edit.add_action(self.line_edit_action, QtWidgets.QLineEdit.ActionPosition.TrailingPosition)

        page_title = QtWidgets.QLabel("Setup ffmpeg")
        page_title.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        ffmpeg_hbox = QtWidgets.QHBoxLayout()
        ffmpeg_hbox.add_widget(self.line_edit)

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(page_title)
        layout.add_layout(ffmpeg_hbox)
        self.set_layout(layout)

    def is_complete(self) -> bool:
        return bool(Path(self.ffmpeg_path).exists() if self.ffmpeg_path else False) and super().is_complete()

    def select_ffmpeg_path(self):
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self,
            caption=self.get_translation("Select ffmpeg directory"),
            dir=str(Config.USER_ROOT)
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)

        if directory_path:
            write_json(
                file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
                data={"root": directory_path},
                create=True
            )
            self.ffmpeg_path = directory_path
            self.line_edit.set_text(directory_path)
            self.completeChanged.emit()

    def get_result(self):
        return self.line_edit.text()


class FinishWizardPage(
    LocalesAccessor,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        label = QtWidgets.QLabel(self.get_translation("Done"))
        label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(label)
        self.set_layout(layout)


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_window_title("Setup wizard")
        self.resize(640, 380)
        self.set_options(
            QtWidgets.QWizard.WizardOption.NoBackButtonOnLastPage
            | QtWidgets.QWizard.WizardOption.NoCancelButtonOnLastPage
        )

        self.pages = (
            LocaleWizardPage(self),
            ThemeWizardPage(self),
            FfmpegWizardPage(self),
            FinishWizardPage(self)
        )

        for page in self.pages:
            self.add_page(page)

        self.button(QtWidgets.QWizard.WizardButton.FinishButton).clicked.connect(self.on_finish)

    def on_finish(self):
        for page in self.pages:
            if hasattr(page, "get_result"):
                page.get_result()

        restart_application()
