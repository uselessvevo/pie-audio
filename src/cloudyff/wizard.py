from PyQt5 import QtWidgets
from cloudykit.utils.files import read_json
from cloudykit.managers.system.manager import System


class LocaleWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        locales = System.config.get('locales.locales')

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet('QComboBox{font-size: 12pt;}')
        self.comboBox.addItems(locales.keys())
        self.comboBox.currentIndexChanged.connect(self.getResult)

        localeLabel = QtWidgets.QLabel('Select locale')
        localeLabel.setStyleSheet('QLabel{font-size: 25pt; padding-bottom: 20px;}')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(localeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        return self.comboBox.currentText()


class ThemeWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        themes = System.config.get('assets.themes')

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet('QComboBox{font-size: 12pt;}')
        self.comboBox.addItems(themes)
        self.comboBox.currentIndexChanged.connect(self.getResult)

        localeLabel = QtWidgets.QLabel('Select theme')
        localeLabel.setStyleSheet('QLabel{font-size: 25pt; padding-bottom: 20px;}')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(localeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        return self.comboBox.currentText()


class FfmpegWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        ffmpegPath = System.userconfig.get('ffmpeg.ffmpeg_path')

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setDisabled(True)
        self.lineEdit.setStyleSheet('QLineEdit{font-size: 15pt;}')

        self.lineEditButton = QtWidgets.QToolButton()
        self.lineEditButton.setStyleSheet('''
            QPushButton{
            font-size: 15pt;
                width: 300px;
                border-radius: 50px;
            }
        ''')
        self.lineEditButton.setText('>')
        self.lineEditButton.clicked.connect(self.selectFfmpegPath)

        localeLabel = QtWidgets.QLabel('Setup ffmpeg')
        localeLabel.setStyleSheet('QLabel{font-size: 25pt; padding-bottom: 20px;}')

        ffmpegHBox = QtWidgets.QHBoxLayout()
        ffmpegHBox.addWidget(self.lineEditButton)
        ffmpegHBox.addWidget(self.lineEdit)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(localeLabel)
        layout.addLayout(ffmpegHBox)
        self.setLayout(layout)

        parent.button(QtWidgets.QWizard.NextButton).clicked.connect(self.checkFfmpegPath)

    def checkFfmpegPath(self):
        pass

    def selectFfmpegPath(self):
        fileDialog = QtWidgets.QFileDialog().getOpenFileName(
            self._parent,
            directory=str(System.user_root)
        )
        if fileDialog:
            print(fileDialog)

    def getResult(self):
        return self.lineEdit.text()


class FinishWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Setup wizard')
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
        self.button(QtWidgets.QWizard.NextButton).clicked.connect(self.onNext)

    def onNext(self):
        if self.currentId() == len(self.pages):
            print('sex')

    def onFinish(self):
        for page in self.pages:
            if hasattr(page, 'getResult'):
                print(page.getResult())
