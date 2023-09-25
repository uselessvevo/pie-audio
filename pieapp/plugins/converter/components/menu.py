from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent: "QObject" = None) -> None:
        super().__init__(parent)

        self._items: list[QAction] = []

        self._menu_hbox_widget = QWidget()

        self._menu_hbox = QHBoxLayout()
        self._menu_hbox.set_contents_margins(1, 1, 1, 1)
        self._menu_hbox.insert_stretch(-1, 1)

        self._menu_hbox_widget.set_layout(self._menu_hbox)
        self._menu_hbox_widget.set_object_name("ConverterMenuWidget")

        self.set_object_name("ConverterItemMenu")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

    def add_item(self, name: str, item: QToolButton) -> None:
        if name in self._items:
            raise PieException(f"Item \"{item}\"")

        item.set_object_name("ConverterMenuItemTB")
        self._menu_hbox.add_widget(item, alignment=Qt.AlignmentFlag.AlignRight)

        self._items[name] = item
