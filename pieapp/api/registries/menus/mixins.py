from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from pieapp.widgets.menus import PieMenu
from pieapp.widgets.menus import PieMenuBar
from pieapp.api.registries.registry import Registry
from pieapp.api.registries.models import SysRegistry, Scope


class MenuAccessorMixin:

    @staticmethod
    def add_menu_bar(
        parent: QWidget = None,
        name: str = None
    ) -> PieMenuBar:
        menu_bar = PieMenuBar(parent)
        return Registry(SysRegistry.Menus).add_menu_bar(name or Scope.Shared, menu_bar)

    @staticmethod
    def get_menu_bar(name: str) -> PieMenuBar:
        return Registry(SysRegistry.Menus).get_menu_bar(name or Scope.Shared)

    @staticmethod
    def add_menu(
        parent: PieMenuBar = None,
        scope: str = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ) -> PieMenu:
        menu = PieMenu(parent=parent, name=name, text=f"&{text}")
        if icon:
            menu.menu_action().set_icon_visible_in_menu(True)
            menu.set_icon(icon)

        return Registry(SysRegistry.Menus).add_menu(scope or Scope.Shared, name, menu)

    @staticmethod
    def add_menu_item(
        scope: str = None,
        menu: str = None,
        name: str = None,
        text: str = None,
        triggered: callable = None,
        icon: QIcon = None,
        before: str = None,
        after: str = None,
        index: Union[int] = None
    ) -> QAction:
        menu_instance: PieMenu = Registry(SysRegistry.Menus).get_menu(scope, menu)
        menu_instance.add_menu_item(name, text, triggered, icon, before, after, index)
        return Registry(SysRegistry.Menus).add_menu_item(scope or Scope.Shared, menu, name, menu_instance)

    @staticmethod
    def get_menu(scope: str, name: str) -> PieMenu:
        return Registry(SysRegistry.Menus).get_menu(scope or Scope.Shared, name)

    @staticmethod
    def get_menu_item(scope: str, menu: str, name: str) -> QAction:
        return Registry(SysRegistry.Menus).get_menu_item(scope, menu, name)
