from PySide6.QtWidgets import QLayout

from pieapp.api.exceptions import PieException
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry


class LayoutRegistry(BaseRegistry):
    name = SysRegistry.Layout

    def init(self) -> None:
        self._layouts: dict[str, QLayout] = {}

    def restore(self, *args, **kwargs):
        self._layouts = {}

    def add(self, name: str, layout: QLayout) -> QLayout:
        if name in self._layouts:
            raise PieException(f"Layout \"{layout}\" already exists")

        self._layouts[name] = layout
        return layout

    def contains(self, name: str) -> bool:
        return name in self._layouts.keys()

    def get(self, name: str) -> QLayout:
        if name not in self._layouts:
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layouts[name]

    def remove(self, name: str) -> None:
        if name not in self._layouts:
            raise PieException(f"Layout \"{name}\" not found")

        del self._layouts[name]
