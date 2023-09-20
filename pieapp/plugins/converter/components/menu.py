from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._actions: list[QAction] = []

        self.set_fixed_height(50)
        self.set_contents_margins(0, 0, 0, 0)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        self._layout = QHBoxLayout()
        self._layout.set_contents_margins(0, 0, 0, 1)
        self._layout.set_alignment(Qt.AlignmentFlag.AlignLeft)
        self.set_layout(self._layout)

        self.set_object_name("ConverterItemMenu")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add_menu_action(self, name: str, action: QAction) -> None:
        if name in self._actions:
            raise PieException(f"Action \"{action}\"")

        self._actions[name] = action
