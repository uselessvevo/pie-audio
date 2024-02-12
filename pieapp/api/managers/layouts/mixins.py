from typing import Any
from PySide6.QtWidgets import QLayout

from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class LayoutsAccessorMixin:

    def add_layout(self, name: str, layout: QLayout) -> Any:
        return Managers(SysManager.Layout).add_layout(name, layout)

    def get_layout(self, name: str) -> Any:
        return Managers(SysManager.Layout).get_layout(name)

    def remove_layout(self, name: str) -> None:
        Managers(SysManager.Layout).remove_layout(name)
