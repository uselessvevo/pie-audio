from PyQt5 import QtWidgets

from cloudykit.managers.system.manager import System


class LocaleWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        self._locales = System.config.get('locales.locales')
        self._cur_locale = System.userconfig.get('locales.locale')
        self._locales_rev = {v: k for (k, v) in self._locales.items()}
        self._cur_locale_rev = self._locales.get(self._cur_locale)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet('QComboBox{font-size: 12pt;}')
        self.comboBox.insertItem(0, self._locales.pop(self._cur_locale))
        self.comboBox.addItems([self._locales.get(i) for (i, _) in self._locales.items()])
        self.comboBox.currentIndexChanged.connect(self.getResult)

        localeLabel = QtWidgets.QLabel(System.locales('Select locale'))
        localeLabel.setStyleSheet('QLabel{font-size: 25pt; padding-bottom: 20px;}')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(localeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        sel_locale = self._locales_rev.get(self.comboBox.currentText())
        if self._cur_locale != sel_locale:
            System.userconfig.save('locales', {'locale': sel_locale})
            # TODO: App need to be restarted
            QtWidgets.QApplication.instance().quit()
        return sel_locale


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
            directory=str(System.userconfig.root)
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
