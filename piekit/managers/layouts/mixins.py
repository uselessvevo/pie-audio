from piekit.layouts.layouts import BaseLayout
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager


class LayoutsAccessorMixin:

    def register_layout(self, layout: BaseLayout) -> None:
        Managers(SysManager.Layouts).register_layout(layout)

    def get_layout(self, name: str) -> BaseLayout:
        return Managers(SysManager.Layouts).get_layout(name)
