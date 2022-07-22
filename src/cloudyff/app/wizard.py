from PyQt5 import QtWidgets


class ThemeWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItem('Python', ' /path/to/filename1')
        self.comboBox.addItem('PyQt5', '/path/to/filename2')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        self.setLayout(layout)


class FfmpegWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Setup wizard')
        self.resize(720, 480)

        pages = (
            ThemeWizardPage(self),
            FfmpegWizardPage(self),
        )

        for page in pages:
            self.addPage(page)
