import os
from typing import Tuple

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from base.messagebox import MessageBox
from cloudykit.utils.os import getScreenInfo


class WindowMixin:
    defaultMinSize: Tuple[int, int] = None
    defaultPosition: Tuple[int, int] = None

    def __init__(
        self,
        config: dict = None,
        *args, **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if os.name == 'nt':
            import ctypes
            myappid = 'mycompany.myproduct.subproduct.version'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self._config = config or dict()

    def setMaximumSize(self, w: int = None, h: int = None) -> None:
        screen = getScreenInfo()
        if not (w, h) > screen:
            w, h = screen

        super().setMaximumSize(QtCore.QSize(w, h))

    def moveToCenter(self):
        rect = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        super().move(rect.topLeft())

    def onCloseEventAccept(self) -> None:
        """ After "Accept" button was pressed """

    def onCloseEventIgnore(self) -> None:
        """ After "Cancel" button was pressed """

    def onCloseEventDefault(self) -> None:
        """ After window was closed """

    def closeEvent(self, event) -> None:
        notification = self._config.get('show_close_notification_on_exit', False)
        if notification:
            message = MessageBox(self)

            if message.clickedButton() == message.yesButton:
                self.onCloseEventAccept()
                event.accept()

            else:
                self.onCloseEventIgnore()
                event.ignore()

        self.onCloseEventDefault()
