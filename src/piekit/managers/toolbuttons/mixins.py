from typing import Union

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QToolButton

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers, Sections


class ToolButtonAccessor:

    def addToolButton(
        self,
        parent: QObject,
        section: Union[str, Sections],
        name: str,
        text: str = None,
        tooltip: str = None,
        icon: QIcon = None,
        triggered: callable = None,
        onlyIcon: bool = False,
    ) -> QToolButton:
        toolButton = QToolButton(parent=parent)
        if icon:
            toolButton.setIcon(icon)

        if tooltip:
            toolButton.setToolTip(tooltip)

        if text:
            toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            toolButton.setText(text)

        if triggered:
            toolButton.clicked.connect(triggered)

        if onlyIcon:
            toolButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            
        return Managers(SysManagers.ToolButton).addToolButton(section or Sections.Shared, name, toolButton)

    def getToolButtons(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManagers.ToolButton).getToolButtons(section, *names)

    def getToolButton(self, section: str, name: str) -> QToolButton:
        return Managers(SysManagers.ToolButton).getToolButton(section or Sections.Shared, name)
