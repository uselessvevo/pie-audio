from PySide6.QtWidgets import QLayout

from pieapp.api.exceptions import PieException
from pieapp.api.managers.base import BaseManager
from pieapp.api.managers.structs import SysManager


class LayoutManager(BaseManager):
    name = SysManager.Layout

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

    def has_layout(self, name: str) -> bool:
        return name in self._layouts.keys()

    def get_layout(self, name: str) -> QLayout:
        if name not in self._layouts:
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layouts[name]

    def remove_layout(self, name: str) -> None:
        if name not in self._layouts:
            raise PieException(f"Layout \"{name}\" not found")

        del self._layouts[name]
