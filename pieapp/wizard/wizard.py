from pathlib import Path

from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog

from piekit.managers.structs import SysManagers, Sections
from piekit.utils.files import writeJson
from piekit.utils.core import restartApplication

from piekit.managers.registry import Managers
from piekit.system import Config


class LocaleWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self._locales = Config.LOCALES
        self._curLocale = Managers(SysManagers.Configs)(
            Sections.User, "locales.locale", Config.DEFAULT_LOCALE
        )
        self._localesRev = {v: k for (k, v) in self._locales.items()}
        self._curLocaleRev = self._locales.get(self._curLocale)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet("QComboBox{font-size: 12pt;}")
        self.comboBox.insertItem(0, self._locales.pop(self._curLocale))
        self.comboBox.addItems([self._locales.get(i) for (i, _) in self._locales.items()])
        self.comboBox.currentIndexChanged.connect(self.getResult)

        self.localeLabel = QtWidgets.QLabel(Managers(SysManagers.Locales)(Sections.Shared, "Select locale"))
        self.localeLabel.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.localeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        newLocale = self._localesRev.get(self.comboBox.currentText())
        writeJson(
            file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "locales.json"),
            data={"locale": newLocale},
            create=True
        )

        if self._curLocale != newLocale:
            restartApplication()

        return newLocale


class ThemeWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet("QComboBox{font-size: 12pt;}")
        self.comboBox.addItems(Managers(SysManagers.Assets).themes)
        self.comboBox.currentIndexChanged.connect(self.getResult)

        self._curTheme = Managers(SysManagers.Configs)(
            Sections.User, "assets.theme", default=Managers(SysManagers.Assets).theme
        )

        themeLabel = QtWidgets.QLabel(Managers(SysManagers.Locales)(Sections.Shared, "Select theme"))
        themeLabel.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(themeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        newTheme = self.comboBox.currentText()
        writeJson(
            file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "assets.json"),
            data={"theme": newTheme},
            create=True
        )

        if self._curTheme != newTheme:
            restartApplication()

        return self.comboBox.currentText()


class FfmpegWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self.ffmpegPath = None

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setDisabled(True)
        self.lineEdit.setStyleSheet("QLineEdit{font-size: 15pt;}")

        self.lineEditButton = QtWidgets.QToolButton()
        self.lineEditButton.setStyleSheet("""
            QPushButton {
                font-size: 15pt;
                width: 300px;
                border-radius: 50px;
            }
        """)
        self.lineEditButton.setIcon(QIcon(
            Managers(SysManagers.Assets)(Sections.Shared, "open-folder.png")
        ))
        self.lineEditButton.clicked.connect(self.selectFfmpegPath)

        pageTitle = QtWidgets.QLabel("Setup ffmpeg")
        pageTitle.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        ffmpegHBox = QtWidgets.QHBoxLayout()
        ffmpegHBox.addWidget(self.lineEditButton)
        ffmpegHBox.addWidget(self.lineEdit)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(pageTitle)
        layout.addLayout(ffmpegHBox)
        self.setLayout(layout)

    def isComplete(self) -> bool:
        return bool(Path(self.ffmpegPath).exists() if self.ffmpegPath else False) and super().isComplete()

    @pyqtSlot()
    def selectFfmpegPath(self):
        directory = QFileDialog(self, Managers(SysManagers.Locales)(Sections.Shared, "Select ffmpeg directory"))
        directory.setFileMode(QFileDialog.DirectoryOnly)
        directory.setOption(QFileDialog.ShowDirsOnly, False)
        directory.getExistingDirectory(directory=str(Config.USER_ROOT))
        directoryPath = directory.directory().path()

        if directoryPath:
            writeJson(
                file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
                data={"root": directoryPath},
                create=True
            )
            self.ffmpegPath = directoryPath
            self.lineEdit.setText(directoryPath)
            self.completeChanged.emit()

    def getResult(self):
        return self.lineEdit.text()


class FinishWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Setup wizard")
        self.resize(640, 380)
        self.setOptions(
            QtWidgets.QWizard.NoBackButtonOnLastPage
            | QtWidgets.QWizard.NoCancelButtonOnLastPage
        )

        self.pages = (
            LocaleWizardPage(self),
            ThemeWizardPage(self),
            FfmpegWizardPage(self),
            FinishWizardPage(self)
        )

        for page in self.pages:
            self.addPage(page)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.onFinish)

    def onFinish(self):
        for page in self.pages:
            if hasattr(page, "getResult"):
                page.getResult()

        restartApplication()
