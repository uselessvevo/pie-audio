from typing import Union

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject
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
        onlyIcon: bool = False
    ) -> QToolButton:
        return Managers(SysManagers.ToolButton).addToolButton(
            parent, section or Sections.Shared, name, text, tooltip, icon, onlyIcon
        )

    def getToolButtons(self, section: str, *names: str) -> list[QObject]:
        return Managers(SysManagers.ToolButton).getToolButtons(section, *names)

    def getToolButton(self, section: str, name: str) -> QToolButton:
        return Managers(SysManagers.ToolButton).getToolButton(section or Sections.Shared, name)
