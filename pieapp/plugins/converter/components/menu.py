from __feature__ import snake_case

from PySide6.QtCore import QSize

from typing import Union
from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout
from pieapp.structs.media import MediaFile

from piekit.exceptions import PieException


class ConverterItemMenu(QWidget):

    def __init__(self, parent: "QObject" = None, media_file: MediaFile = None) -> None:
        super().__init__(parent)

        self._media_file = media_file

        self._items_dict: dict[str, QToolButton] = {}
        self._items_list: list[tuple[str, QToolButton]] = []

        self._menu_hbox = QHBoxLayout()
        self._menu_hbox.set_contents_margins(5, 5, 5, 5)
        self._menu_hbox.insert_stretch(-1, 1)

        self.set_layout(self._menu_hbox)
        self.set_object_name("ConverterMenuWidget")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)
        menu_size_policy = self.size_policy()
        menu_size_policy.set_retain_size_when_hidden(True)
        self.set_size_policy(menu_size_policy)
        self.hide()

    @property
    def items(self) -> list[QToolButton]:
        return list(self._items_dict.values())

    def add_item(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
    ) -> QToolButton:
        """
        This method allows us to register a tool button on the shorcuts menu

        Args:
            * name (str): Button name
            * text (str): Text displayed on tool button
            * icon (QIcon): Icon displayed on tool button
            * callback (callable|None): Method to call on button click event. Requires `media_file:<MediaFile>`
            * before (str): Display a button before passed button
            * after (str): Display a button after passed button
        """
        if name in self._items_dict:
            raise PieException(f"Item \"{name}\" is already registered")

        tool_button = QToolButton()
        tool_button.set_text(text)
        tool_button.set_icon(icon)
        tool_button.set_icon_size(QSize(14, 14))
        tool_button.set_object_name("ConverterMenuItemTB")
        tool_button.clicked.connect(lambda: callback(self._media_file))

        self._items_dict[name] = tool_button

        item_index: Union[int, None] = None
        if before:
            item_index = self._items_list.index((before, self._items_dict[before]))
        elif after:
            item_index = self._items_list.index((after, self._items_dict[after])) + 1

        if item_index is not None:
            self._items_list.insert(item_index, (name, tool_button))
            self._menu_hbox.insert_widget(item_index, tool_button, alignment=Qt.AlignmentFlag.AlignRight)
        else:
            self._items_list.append((name, tool_button))
            self._menu_hbox.add_widget(tool_button, alignment=Qt.AlignmentFlag.AlignRight)

        return tool_button
