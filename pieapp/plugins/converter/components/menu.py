from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Dict of actions: {<action name>: <QAction instance>, ...}
        self._actions: dict[str, QAction] = {}

    def add_menu_action(self, name: str, action: QAction) -> None:
        if name in self._actions:
            raise PieException(f"Action \"{action}\"")

        self._actions[name] = action
