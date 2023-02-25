from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


class ActionMixin:

    def registerAction(self, text: str, icon: QIcon, func: callable, *funcargs, **funckwargs) -> None:
        action = QAction(text, icon, self)
        action.triggered.connect(func(*funcargs, **funckwargs))
