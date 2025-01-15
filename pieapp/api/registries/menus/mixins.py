from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from pieapp.api.registries.menus.registry import MenuRegistry
from pieapp.widgets.menus import PieMenu
from pieapp.widgets.menus import PieMenuBar
from pieapp.api.models.scopes import Scope


class MenuAccessorMixin:

    def add_menu_bar(self, name: str = None) -> PieMenuBar:
        menu_bar = PieMenuBar()
        return MenuRegistry.add_menu_bar(name or Scope.Shared, menu_bar)

    def get_menu_bar(self, name: str) -> PieMenuBar:
        return MenuRegistry.get_menu_bar(name or Scope.Shared)

    def add_menu(
        self,
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

        return MenuRegistry.add_menu(scope or Scope.Shared, name, menu)

    def add_menu_item(
        self,
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
        menu_instance: PieMenu = MenuRegistry.get_menu(scope, menu)
        menu_instance.add_menu_item(name, text, triggered, icon, before, after, index)
        return MenuRegistry.add_menu_item(scope or Scope.Shared, menu, name, menu_instance)

    def get_menu(self, scope: str, name: str) -> PieMenu:
        return MenuRegistry.get_menu(scope or Scope.Shared, name)

    def get_menu_item(self, scope: str, menu: str, name: str) -> QAction:
        return MenuRegistry.get_menu_item(scope, menu, name)
