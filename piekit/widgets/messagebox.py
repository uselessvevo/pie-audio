from PySide6.QtGui import Qt
from __feature__ import snake_case

from PySide6.QtWidgets import QMessageBox, QCheckBox, QVBoxLayout, QSpacerItem
from PySide6.QtWidgets import QPushButton

from piekit.managers.structs import Section
from piekit.managers.locales.mixins import LocalesAccessorMixin


class MessageCheckBox(QMessageBox, LocalesAccessorMixin):
    section = Section.Shared

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.set_style_sheet("QLabel{min-width: 300px; min-height: 50}")
        self.set_window_title(self.get_translation("Exit"))
        self.set_text(self.get_translation("Are you sure you want to exit?"))

        self.yes_button = QPushButton()
        self.yes_button.set_text(self.get_translation("Yes"))

        self.no_button = QPushButton()
        self.no_button.set_text(self.get_translation("No"))

        self.add_button(self.yes_button, QMessageBox.ButtonRole.YesRole)
        self.add_button(self.no_button, QMessageBox.ButtonRole.NoRole)
        self.set_default_button(self.no_button)

        self.set_window_modality(Qt.WindowModality.NonModal)
        self.check_box = QCheckBox(self)
        self.set_check_box(self.check_box)

    def is_checked(self) -> bool:
        return self.check_box.is_checked()

    def set_checked(self, state: bool) -> None:
        self.check_box.set_checked(state)

    def set_check_box_text(self, text: str) -> None:
        self.check_box.set_text(text)
