from __feature__ import snake_case

from functools import partial

from PySide6.QtWidgets import QWidget, QLayout

from piekit.exceptions import PieException
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class LayoutsAccessorMixin:

    def add_layout(self, name: str, layout: QLayout) -> QLayout:
        return Managers(SysManager.Layouts).add_layout(name, layout)

    def get_layout(self, name: str) -> QLayout:
        return Managers(SysManager.Layouts).get_layout(name)

    def remove_layout(self, name: str) -> None:
        Managers(SysManager.Layouts).remove_layout(name)
