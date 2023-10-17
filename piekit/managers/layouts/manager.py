from PySide6.QtWidgets import QLayout

from piekit.exceptions import PieException
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager


class LayoutManager(BaseManager):
    name = SysManager.Layouts

    def __init__(self) -> None:
        self._layouts: dict[str, QLayout] = {}

    def shutdown(self, *args, **kwargs):
        self._layouts = {}

    def reload(self):
        self.shutdown()
        self.init()

    def add_layout(self, name: str, layout: QLayout) -> QLayout:
        if name in self._layouts:
            raise PieException(f"Layout \"{layout}\" already exists")

        self._layouts[name] = layout
        return layout

    def get_layout(self, name: str) -> QLayout:
        if name not in self._layouts:
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layouts[name]

    def remove_layout(self, name: str) -> None:
        if name not in self._layouts:
            raise PieException(f"Layout \"{name}\" not found")

        del self._layouts[name]
