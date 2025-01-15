from __feature__ import snake_case

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QToolButton


def create_tool_button(
    parent=None,
    text: str = None,
    tooltip: str = None,
    icon: QIcon = None,
    triggered: callable = None,
    only_icon: bool = False,
    focus_type: Qt.FocusPolicy = Qt.FocusPolicy.NoFocus,
    icon_size: tuple[int, int] = (25, 25),
    object_name: str = None
) -> QToolButton:
    tool_button = QToolButton(parent=parent)
    if icon:
        tool_button.set_icon(icon)

    if tooltip:
        tool_button.set_tool_tip(tooltip)

    if text:
        # tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonIconOnly)
        tool_button.set_text(text)

    if triggered:
        tool_button.clicked.connect(triggered)

    if only_icon:
        tool_button.set_tool_button_style(Qt.ToolButtonStyle.ToolButtonIconOnly)

    if object_name:
        tool_button.set_object_name(object_name)

    tool_button.set_focus_policy(focus_type)
    tool_button.set_icon_size(QSize(*icon_size or (24, 24)))

    return tool_button
