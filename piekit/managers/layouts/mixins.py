from typing import Any
from PySide6.QtWidgets import QLayout

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class LayoutsAccessorMixin:

    def add_layout(self, name: str, layout: QLayout) -> Any:
        return Managers(SysManager.Layouts).add_layout(name, layout)

    def get_layout(self, name: str) -> Any:
        return Managers(SysManager.Layouts).get_layout(name)

    def remove_layout(self, name: str) -> None:
        Managers(SysManager.Layouts).remove_layout(name)
