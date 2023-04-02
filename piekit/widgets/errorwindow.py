import sys
from typing import Union

from piekit.utils.logger import logger

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QErrorMessage

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QPushButton


def ErrorWindow(err_type: Union[Exception, str], err_value: str, err_traceback: Union[str, list]):
    """
    A window will close after it initialization
    """
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxWarning))

    if isinstance(err_traceback, (tuple, list)):
        err_traceback = '<br><br>'.join(i for i in err_traceback)

    window = QErrorMessage()
    window.finished.connect(lambda e: app.quit)

    window.resize(600, 350)

    window.findChild(QLabel, '').setVisible(False)
    window.findChild(QCheckBox, '').setVisible(False)
    window.findChild(QPushButton, '').setVisible(False)
    window.setWindowTitle(f'{err_type} {err_value}')
    window.showMessage(err_traceback)

    logger.error(err_type, err_value)

    sys.exit(app.exec())
