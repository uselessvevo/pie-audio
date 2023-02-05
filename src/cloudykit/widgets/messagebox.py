from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton

from cloudykit.system import System


class MessageBox(QMessageBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.trans = System.registry.locales

        self.setStyleSheet("QLabel{min-width: 300px; min-height: 50}")
        self.setWindowTitle(self.trans('Exit'))
        self.setText(self.trans("Are you sure you want to exit?"))  # Are you sure you want to quit?

        self.yesButton = QPushButton()
        self.yesButton.setText(self.trans("Yes"))

        self.noButton = QPushButton()
        self.noButton.setText(self.trans("No"))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
