import sys
from typing import Union

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QErrorMessage

    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtWidgets import QStyle
    from PyQt5.QtWidgets import QCheckBox
    from PyQt5.QtWidgets import QPushButton

    def SystemError(err_type: Union[Exception, str], err_value: str, err_traceback: Union[str, list]):
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

        sys.exit(app.exec_())

except ImportError:
    try:
        import tkinter as tk
        import tkinter.messagebox

        def SystemError(err_type: Union[Exception, str], err_value: str, err_traceback: Union[str, list]):
            root = tk.Tk()
            root.overrideredirect(1)
            root.withdraw()
            tkinter.messagebox.showerror(master=root, title=f'{err_type} {err_value}', message=err_traceback)

    except ImportError:
        def SystemError(err_type: Union[Exception, str], err_value: str, err_traceback: Union[str, list]):
            raise err_type