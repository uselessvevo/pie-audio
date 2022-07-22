from PyQt5 import QtWidgets


class ThemeWizardPage(QtWidgets.QWizardPage):

    def setup(self):
        pass


class FfmpegWizardPage(QtWidgets.QWizardPage):

    def setup(self):
        pass


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        pages = (
            ThemeWizardPage(self),
            FfmpegWizardPage(self),
        )

        for page in pages:
            page.setup()
