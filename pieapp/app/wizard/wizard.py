from __feature__ import snake_case

import os

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QStyle

from pieapp.api.gloader import Global
from pieapp.utils.qt import restart_application
from pieapp.api.registries.models import Scope
from pieapp.api.registries.locales.helpers import translate

from pieapp.app.wizard.pages.converter import ConverterWizardPage
from pieapp.app.wizard.pages.locale import LocaleWizardPage
from pieapp.app.wizard.pages.theme import ThemeWizardPage


class FinishWizardPage(QtWidgets.QWizardPage):
    scope = Scope.Shared

    def __init__(self, parent) -> None:
        super().__init__(parent)

        label = QtWidgets.QLabel(f'{translate("Done")}!')
        label.set_style_sheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.add_widget(label)
        self.set_layout(layout)


class StartupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_window_title(translate("Setup Wizard", scope=Scope.Shared))
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
        self.set_wizard_style(QtWidgets.QWizard.WizardStyle.ModernStyle)

        self.pages: list[QtWidgets.QWizardPage] = [
            LocaleWizardPage(self),
            ThemeWizardPage(self),
            ConverterWizardPage(self),
            FinishWizardPage(self)
        ]

        for page in self.pages:
            self.add_page(page)

        self.button(QtWidgets.QWizard.WizardButton.FinishButton).clicked.connect(self.on_finish)

    def on_finish(self):
        for page in self.pages:
            if hasattr(page, "finish"):
                page.finish()

        restart_application()
        settings = QSettings()
        settings.set_value("first_run", False)
