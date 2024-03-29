from typing import Union

from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QWidget

from pieapp.widgets.menus import PieMenu, INDEX_END, INDEX_START
from pieapp.api.managers.registry import Registries
from pieapp.api.managers.structs import SysRegistry, Section


class MenuAccessorMixin:

    def add_menu_bar(
        self,
        parent: QWidget = None,
        name: str = None
    ) -> QMenuBar:
        menu_bar = QMenuBar(parent)
        return Registries(SysRegistry.Menus).add_menu_bar(name or Section.Shared, menu_bar)

    def get_menu_bar(self, name: str) -> QMenuBar:
        return Registries(SysRegistry.Menus).get_menu_bar(name or Section.Shared)

    def add_menu(
        self,
        parent: QMenuBar = None,
        section: str = None,
        name: str = None,
        text: str = None,
        icon: QIcon = None,
    ) -> PieMenu:
        menu = PieMenu(parent=parent, name=name, text=f"&{text}")
        if icon:
            menu.menu_action().set_icon_visible_in_menu(True)
            menu.set_icon(icon)

        return Registries(SysRegistry.Menus).add_menu(section or Section.Shared, name, menu)

    def add_menu_item(
        self,
        section: str = None,
        menu: str = None,
        name: str = None,
        text: str = None,
        triggered: callable = None,
        icon: QIcon = None,
        before: str = None,
        index: Union[int, INDEX_START, INDEX_END] = None
    ) -> QAction:
        manager = Registries(SysRegistry.Menus)
        menu_instance = manager.get_menu(section, menu)
        menu_instance.add_menu_item(name, text, triggered, icon, before, index)
        return manager.add_menu_item(section or Section.Shared, menu, name, menu_instance)

    def get_menu(self, section: str, name: str) -> PieMenu:
        return Registries(SysRegistry.Menus).get_menu(section or Section.Shared, name)

    def get_menu_item(self, section: str, menu: str, name: str) -> QAction:
        return Registries(SysRegistry.Menus).get_menu_item(section, menu, name)
