from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton

from cloudykit.system.manager import System


class MessageBox(QMessageBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.trans = System.locales

        self.setStyleSheet('QLabel{min-width: 300px; min-height: 50}')
        self.setWindowTitle(self.trans('Shared.Exit'))
        self.setText(self.trans('Shared.ExitMessage'))

        self.yesButton = QPushButton()
        self.yesButton.setText(self.trans('Shared.Yes'))

        self.noButton = QPushButton()
        self.noButton.setText(self.trans('Shared.No'))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
