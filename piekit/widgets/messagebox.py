from __feature__ import snake_case

from PySide6.QtGui import Qt

from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox, QCheckBox

from piekit.managers.locales.helpers import translate


class MessageCheckBox(QMessageBox):

    def __init__(
        self,
        parent: "QObject" = None,
        window_title: str = "Title",
        message_text: str = "Message",
        yes_button_text: str = "Yes",
        no_button_text: str = "No"
    ) -> None:
        super().__init__(parent)

        self.set_style_sheet("QLabel{min-width: 300px; min-height: 50}")
        self.set_window_title(translate(window_title))
        self.set_text(translate(message_text))

        self.yes_button = QPushButton()
        self.yes_button.set_text(translate(yes_button_text))

        self.no_button = QPushButton()
        self.no_button.set_text(translate(no_button_text))

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
