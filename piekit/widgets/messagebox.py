from __feature__ import snake_case

from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton

from piekit.managers.structs import Sections
from piekit.managers.locales.mixins import LocalesAccessor


class MessageBox(QMessageBox, LocalesAccessor):
    section = Sections.Shared

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.set_style_sheet("QLabel{min-width: 300px; min-height: 50}")
        self.set_window_title(self.get_translation('Exit'))
        self.set_text(self.get_translation("Are you sure you want to exit?"))

        self.yes_button = QPushButton()
        self.yes_button.set_text(self.get_translation("Yes"))

        self.no_button = QPushButton()
        self.no_button.set_text(self.get_translation("No"))

        self.add_button(self.yes_button, QMessageBox.ButtonRole.YesRole)
        self.add_button(self.no_button, QMessageBox.ButtonRole.NoRole)
        self.set_default_button(self.no_button)

        self.exec()
