from __feature__ import snake_case

from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Slot, Signal
from PySide6.QtWidgets import QWidget, QToolButton
from PySide6.QtWidgets import QHBoxLayout

from pieapp.api.converter.models import MediaFile
from pieapp.api.registries.locales.helpers import translate


class QuickActionSideMenu(QWidget):

    def __init__(self, parent: "QObject") -> None:
        super().__init__(parent)


class QuickActionMenu(QWidget):

    def __init__(self, parent: "QObject", media_file_name: str) -> None:
        super().__init__(parent)

        self._media_file_name = media_file_name
        self._items_dict: dict[str, QToolButton] = {}
        self._items_list: list[tuple[str, QToolButton]] = []

        self._menu_hbox = QHBoxLayout(self)
        self._menu_hbox.set_contents_margins(1, 1, 1, 1)
        self._menu_hbox.insert_stretch(-1, 1)

        self.set_layout(self._menu_hbox)
        self.set_object_name("QuickAction")
        self.set_attribute(Qt.WidgetAttribute.WA_StyledBackground)

        menu_size_policy = self.size_policy()
        menu_size_policy.set_retain_size_when_hidden(True)
        self.set_size_policy(menu_size_policy)
        self.hide()

    def get_items(self) -> list[QToolButton]:
        return list(self._items_dict.values())

    def add_item(
        self,
        name: str,
        text: str,
        icon: QIcon,
        callback: callable = None,
        before: str = None,
        after: str = None,
        enabled: bool = True
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
            * enabled (bool): Enable button or not. Default is `True`
        """
        if self._items_dict.get(name):
            return

        tool_button = QToolButton()
        if enabled is False:
            tool_button.set_tool_tip(translate("Plugin doesn't support this file format"))

        tool_button.set_enabled(enabled)
        tool_button.set_text(text)
        tool_button.set_icon(icon)
        tool_button.set_icon_size(QSize(14, 14))
        tool_button.set_object_name("QuickActionToolButton")
        tool_button.clicked.connect(callback)

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
