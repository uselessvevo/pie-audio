from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry, Section
from pieapp.widgets.toolbars import PieToolBar


class ToolBarAccessorMixin:

    def add_toolbar(
        self,
        parent: QObject = None,
        name: str = None
    ) -> PieToolBar:
        toolbar = PieToolBar(parent=parent, name=name)
        return Registries(SysRegistry.ToolBars).add_toolbar(name or Section.Shared, toolbar)

    def add_toolbar_item(
        self,
        toolbar: str = None,
        name: str = None,
        item: Union[QWidget, QAction] = None,
        after: str = None,
        before: str = None
    ) -> Union[QAction, QWidget]:
        manager = Registries(SysRegistry.ToolBars)
        toolbar_instance: PieToolBar = manager.get_toolbar(toolbar)
        toolbar_instance.add_toolbar_item(name, item, after, before)
        return manager.add_item(toolbar or Section.Shared, name, item)

    def get_toolbar_item(self, section: str, name: str) -> QWidget:
        return Registries(SysRegistry.ToolBars).get_item(section, name)

    def get_toolbar_items(self, section: str, *names: str) -> list[QObject]:
        return Registries(SysRegistry.ToolBars).get_items(section, *names)

    def get_toolbar(self, name: str) -> PieToolBar:
        return Registries(SysRegistry.ToolBars).get_toolbar(name)

    def get_toolbars(self, *names: str) -> list[PieToolBar]:
        return Registries(SysRegistry.ToolBars).get_toolbars(*names)
