from __feature__ import snake_case

import os
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtCore import QDir, QSettings
from PySide6.QtWidgets import QFileDialog, QStyle
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from piekit.managers.structs import SysManager, Section
from piekit.utils.core import restart_application

from piekit.managers.registry import Managers
from piekit.globals import Global


class LocaleWizardPage(
    ConfigAccessorMixin,
    LocalesAccessorMixin,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self._locales = Global.LOCALES
        self._cur_locale = self.get_config(
            key="locale.locale",
            default=Global.DEFAULT_LOCALE,
            scope=Section.Root,
            section=Section.User
        )
        self._locales_reversed = {v: k for (k, v) in self._locales.items()}

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 12pt;}")
        self.combo_box.insert_item(0, self._locales.pop(self._cur_locale))
        self.combo_box.add_items([self._locales.get(i) for (i, _) in self._locales.items()])
        self.combo_box.currentIndexChanged.connect(self.get_result)

        self.locale_label = QtWidgets.QLabel(self.translate("Select locale"))
        self.locale_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(self.locale_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def get_result(self):
        new_locale = self._locales_reversed.get(self.combo_box.current_text())
        self.set_config(
            key="locale",
            data={"locale": new_locale},
            scope=Section.Root,
            section=Section.User
        )
        self.save_config(
            scope=Section.Root,
            section=Section.User,
            create=True
        )

        if self._cur_locale != new_locale:
            restart_application()

        return new_locale


class ThemeWizardPage(
    ConfigAccessorMixin,
    LocalesAccessorMixin,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.set_style_sheet("QComboBox{font-size: 12pt;}")
        self.combo_box.add_items(Managers(SysManager.Themes).get_themes())
        self.combo_box.currentIndexChanged.connect(self.get_result)

        self._cur_theme = self.get_config(
            key="assets.theme",
            default=Managers(SysManager.Themes).get_theme(),
            scope=Section.Root,
            section=Section.User
        )

        theme_label = QtWidgets.QLabel(self.translate("Select theme"))
        theme_label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(theme_label)
        layout.add_widget(self.combo_box)
        self.set_layout(layout)

    def get_result(self):
        new_theme = self.combo_box.current_text()
        self.set_config(
            scope=Section.Root,
            section=Section.User,
            key="assets.theme",
            data=new_theme
        )
        self.save_config(
            scope=Section.Root,
            section=Section.User
        )

        if self._cur_theme != new_theme:
            restart_application()

        return self.combo_box.current_text()


class ConverterWizardPage(
    LocalesAccessorMixin,
    ConfigAccessorMixin,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self.ffmpeg_path = None

        self.line_edit_action = QAction()
        self.line_edit_action.set_icon(self.style().standard_icon(QStyle.StandardPixmap.SP_DirIcon))
        self.line_edit_action.triggered.connect(self.select_ffmpeg_root_path)

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.set_style_sheet("QLineEdit{font-size: 15pt;}")
        self.line_edit.add_action(self.line_edit_action, QtWidgets.QLineEdit.ActionPosition.TrailingPosition)

        page_title = QtWidgets.QLabel(self.translate("Setup ffmpeg"))
        page_title.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        ffmpeg_hbox = QtWidgets.QHBoxLayout()
        ffmpeg_hbox.add_widget(self.line_edit)

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(page_title)
        layout.add_layout(ffmpeg_hbox)
        self.set_layout(layout)

    def is_complete(self) -> bool:
        return bool(Path(self.ffmpeg_path).exists() if self.ffmpeg_path else False) and super().is_complete()

    def select_ffmpeg_root_path(self):
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self,
            caption=self.translate("Select ffmpeg directory"),
            dir=str(Global.USER_ROOT)
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)

        if directory_path:
            self.set_config(
                scope=Section.Root,
                section=Section.User,
                key="ffmpeg.root",
                data=directory_path
            )

            binaries = list(map(Path, ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe")))
            for binary in binaries:
                if not (directory_path / binary).exists():
                    raise FileNotFoundError(f"Binary file \"{binary.stem!s}\" not found. "
                                            f"Please, download ffmpeg bundle from https://ffmpeg.org/download.html")

                self.set_config(
                    scope=Section.Root,
                    section=Section.User,
                    key=f"ffmpeg.{binary.stem!s}",
                    data=str(directory_path / binary)
                )

            self.save_config(
                scope=Section.Root,
                section=Section.User
            )
            self.ffmpeg_path = directory_path
            self.line_edit.set_text(directory_path)
            self.completeChanged.emit()

    def get_result(self):
        return self.line_edit.text()


class FinishWizardPage(
    LocalesAccessorMixin,
    QtWidgets.QWizardPage
):
    section = Section.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        label = QtWidgets.QLabel(self.translate("Done"))
        label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(label)
        self.set_layout(layout)


class SetupWizard(QtWidgets.QWizard, LocalesAccessorMixin):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_window_title(self.translate("Setup Wizard", Section.Shared))
        self.set_window_icon(self.style().standard_icon(QStyle.StandardPixmap.SP_DialogHelpButton))

        if os.name == "nt":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                Global.PIEAPP_ORGANIZATION_DOMAIN
            )

        self.resize(640, 380)
        self.set_options(
            QtWidgets.QWizard.WizardOption.NoBackButtonOnLastPage
            | QtWidgets.QWizard.WizardOption.NoCancelButtonOnLastPage
        )

        self.pages = (
            LocaleWizardPage(self),
            ThemeWizardPage(self),
            ConverterWizardPage(self),
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
        settings = QSettings()
        settings.set_value("fully_setup", True)
