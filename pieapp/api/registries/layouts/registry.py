from typing import Union

from PySide6.QtWidgets import QLayout

from pieapp.api.exceptions import PieError
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry


class LayoutRegistryClass(BaseRegistry):
    name = SysRegistry.Layout

    def init(self) -> None:
        # Dictionary of layouts
        # Structure: <layout name>: "layout": <layout>, "parent": <parent_layout>
        self._layouts: dict = {}

    def restore(self, *args, **kwargs):
        self._layouts = {}

    def add(self, name: str, layout: QLayout, parent_layout_name: QLayout) -> QLayout:
        if name in self._layouts:
            raise PieError(f"Layout \"{layout}\" already exists")

        self._layouts[name] = {"layout": layout, "parent": parent_layout_name}
        return layout

    def get_children(self, name: str) -> list[QLayout]:
        if name not in self._layouts:
            raise PieError(f"Layout {name} not found")

        return [i for i in self._layouts if i["parent"] == name]

    def contains(self, name: str) -> bool:
        return name in self._layouts.keys()

    def get(self, name: str, key: str = "layout") -> QLayout:
        if name not in self._layouts:
            raise PieError(f"Can't find layout \"{name}\"")

        return self._layouts[name]["layout"]

    def remove(self, name: str) -> None:
        if name not in self._layouts:
            raise PieError(f"Layout \"{name}\" not found")

        del self._layouts[name]


LayoutRegistry = LayoutRegistryClass()
