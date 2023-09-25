from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent: "QObject" = None) -> None:
        super().__init__(parent)

        self._items: dict[str, QToolButton] = {}

        self._menu_hbox = QHBoxLayout()
        self._menu_hbox.set_contents_margins(1, 1, 1, 1)
        self._menu_hbox.insert_stretch(-1, 1)

        self.set_layout(self._menu_hbox)
        self.set_object_name("ConverterMenuWidget")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add_item(self, name: str, item: QToolButton) -> None:
        if name in self._items:
            raise PieException(f"Item \"{item}\"")

        item.set_object_name("ConverterMenuItemTB")
        self._menu_hbox.add_widget(item, alignment=Qt.AlignmentFlag.AlignRight)

        self._items[name] = item
