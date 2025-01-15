from __feature__ import snake_case

from PySide6.QtGui import Qt

from PySide6.QtWidgets import QMessageBox, QCheckBox

from pieapp.api.utils.qapp import get_application
from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole


class MessageBox(QMessageBox):

    def __init__(
        self,
        parent: "QObject" = None,
        window_title: str = "Title",
        message_text: str = "Message",
        yes_button_text: str = "Yes",
        no_button_text: str = "No",
        show_checkbox: bool = True,
        show_close_button: bool = True
    ) -> None:
        super().__init__(parent)

        if show_close_button is False:
            flags = self.window_flags()
            flags &= Qt.WindowType.CustomizeWindowHint
            flags &= ~Qt.WindowType.WindowCloseButtonHint
            self.set_window_flags(flags)

        self.set_style_sheet("QLabel{min-width: 300px; min-height: 50}")
        self.set_window_title(window_title)
        self.set_text(message_text)

        self.yes_button = Button(ButtonRole.Primary)
        self.yes_button.set_text(yes_button_text)

        self.no_button = Button()
        self.no_button.set_text(no_button_text)

        self.add_button(self.yes_button, QMessageBox.ButtonRole.YesRole)
        self.add_button(self.no_button, QMessageBox.ButtonRole.NoRole)
        self.set_default_button(self.no_button)

        self.set_window_modality(Qt.WindowModality.NonModal)
        self.check_box = None
        if show_checkbox:
            self.check_box = QCheckBox(self)
            self.set_check_box(self.check_box)

    def close_event(self, event) -> None:
        get_application().exit()

    def is_checked(self) -> bool:
        return self.check_box.is_checked()

    def set_checked(self, state: bool) -> None:
        self.check_box.set_checked(state)

    def set_check_box_text(self, text: str) -> None:
        if self.check_box is not None:
            self.check_box.set_text(text)

    def set_close_event(self, trigger: callable = None) -> None:
        if trigger is None:
            get_application().quit()
