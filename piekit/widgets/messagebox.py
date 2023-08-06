from __feature__ import snake_case

from PySide6.QtWidgets import QMessageBox, QCheckBox
from PySide6.QtWidgets import QPushButton

from piekit.managers.structs import Section
from piekit.managers.locales.mixins import LocalesAccessorMixin


class MessageBox(QMessageBox, LocalesAccessorMixin):
    section = Section.Shared

    def __init__(self, parent=None, show_check_box: bool = False) -> None:
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

        if show_check_box:
            check_box = QCheckBox(self.get_translation("Don't show this message again"))
            self.set_check_box(check_box)

        self.exec()
