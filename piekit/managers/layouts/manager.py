from piekit.exceptions import PieException
from piekit.layouts.layouts import BaseLayout
from piekit.managers.base import BaseManager
from piekit.managers.structs import SysManager


class LayoutManager(BaseManager):
    name = SysManager.Layouts

    def __init__(self) -> None:
        self._layouts: dict[str, BaseLayout] = {}

    def shutdown(self, *args, **kwargs):
        self._layouts = {}

    def reload(self):
        self.shutdown()
        self.init()

    def register_layout(self, layout: BaseLayout) -> None:
        if layout.name in self._layouts:
            raise PieException(f"Layout \"{layout}\" already exists")

        self._layouts[layout.name] = layout

    def get_layout(self, name: str) -> BaseLayout:
        if name not in self._layouts:
            raise PieException(f"Can't find layout \"{name}\"")

        return self._layouts[name]
