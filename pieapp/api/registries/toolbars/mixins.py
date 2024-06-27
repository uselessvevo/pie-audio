from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry

from pieapp.widgets.toolbars import PieToolBar


class ToolBarAccessorMixin:

    def add_toolbar(
        self,
        parent: QObject = None,
        name: str = None,
    ) -> PieToolBar:
        toolbar = PieToolBar(parent, name)
        return Registry(SysRegistry.ToolBars).add_toolbar(name or Scope.Shared, toolbar)

    def add_toolbar_item(
        self,
        toolbar: str = None,
        name: str = None,
        item: Union[QWidget, QAction] = None,
        after: str = None,
        before: str = None
    ) -> Union[QAction, QWidget]:
        manager = Registry(SysRegistry.ToolBars)
        toolbar_instance: PieToolBar = manager.get_toolbar(toolbar)
        toolbar_instance.add_toolbar_item(name, item, after, before)
        return manager.add_item(toolbar or Scope.Shared, name, item)

    def get_toolbar_item(self, scope: str, name: str) -> QWidget:
        return Registry(SysRegistry.ToolBars).get_item(scope, name)

    def get_toolbar_items(self, scope: str, *names: str) -> list[QObject]:
        return Registry(SysRegistry.ToolBars).items(scope, *names)

    def get_toolbar(self, name: str) -> PieToolBar:
        return Registry(SysRegistry.ToolBars).get_toolbar(name)

    def get_toolbars(self, *names: str) -> list[PieToolBar]:
        return Registry(SysRegistry.ToolBars).get_toolbars(*names)
