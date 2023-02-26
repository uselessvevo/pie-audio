from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton

from piekit.managers.types import Sections
from piekit.managers.locales.mixins import LocalesAccessor


class MessageBox(QMessageBox, LocalesAccessor):
    section = Sections.Shared

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setStyleSheet("QLabel{min-width: 300px; min-height: 50}")
        self.setWindowTitle(self.getTranslation('Exit'))
        self.setText(self.getTranslation("Are you sure you want to exit?"))

        self.yesButton = QPushButton()
        self.yesButton.setText(self.getTranslation("Yes"))

        self.noButton = QPushButton()
        self.noButton.setText(self.getTranslation("No"))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
