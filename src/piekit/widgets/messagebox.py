from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections


class MessageBox(QMessageBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setStyleSheet("QLabel{min-width: 300px; min-height: 50}")
        self.setWindowTitle(Managers(SysManagers.Locales)(Sections.Shared, 'Exit'))
        self.setText(Managers(SysManagers.Locales)(Sections.Shared, "Are you sure you want to exit?"))

        self.yesButton = QPushButton()
        self.yesButton.setText(Managers(SysManagers.Locales)(Sections.Shared, "Yes"))

        self.noButton = QPushButton()
        self.noButton.setText(Managers(SysManagers.Locales)(Sections.Shared, "No"))

        self.addButton(self.yesButton, QMessageBox.YesRole)
        self.addButton(self.noButton, QMessageBox.NoRole)
        self.setDefaultButton(self.noButton)

        self.exec_()
