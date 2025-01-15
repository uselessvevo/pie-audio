from typing import Union

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

from pieapp.api.models.scopes import Scope
from pieapp.api.registries.sysregs import SysRegistry
from pieapp.api.registries.registry import RegistryContainer
from pieapp.api.registries.toolbars.registry import ToolBarRegistry
from pieapp.widgets.toolbars.toolbars import PieToolBar


class ToolBarAccessorMixin:
    """
    ToolBarAccessorMixin allows you to store all toolbars and their items (widgets; QToolButton f.e.)
    Optionally requires `TabRegistry` to add toolbar into tab
    """

    @staticmethod
    def add_toolbar(toolbar_name: str, tab_name: str = None) -> PieToolBar:
        """
        Create PieToolBar and register it in ToolBarRegistry.
        Also, you can render toolbar on PieTab and add it in TabRegistry if `tab_name` is `str`.

        Args:
            toolbar_name (str): toolbar name to register it in ToolBarRegistry
            tab_name (str|None): tab name to render and register toolbar in PieTab and TabRegistry

        Returns:
            PieToolBar
        """
        toolbar = PieToolBar(toolbar_name)
        if tab_name is str:
            tab_registry = RegistryContainer.get_registry(SysRegistry.Tabs)
            if tab_registry is not None:
                tab_registry.add_tab_item(tab_name, toolbar_name, toolbar)
        else:
            return ToolBarRegistry.add_toolbar(toolbar_name, toolbar)

    @staticmethod
    def add_toolbar_item(
        toolbar_name: str,
        item_name: str,
        item_widget: Union[QWidget, QAction],
        after: str = None,
        before: str = None
    ) -> Union[QAction, QWidget]:
        """
        Render widget on PieToolBar and register it in ToolBarRegistry

        Args:
            toolbar_name (str): toolbar name to register item on it
            item_name (str): item name to register it in ToolBarRegistry
            item_widget (QWidget|QAction):
            after (str): name of the toolbar item to register it after given item name
            before (str): name of the toolbar item to register it before given item name
        """
        toolbar = ToolBarRegistry.get_toolbar(toolbar_name)
        toolbar.add_item(item_name, item_widget, after, before)
        return ToolBarRegistry.add_toolbar_item(toolbar_name or Scope.Shared, item_name, item_widget)

    @staticmethod
    def get_toolbar_item(toolbar_name: str, item_name: str) -> Union[QWidget, QAction]:
        """
        Get toolbar item

        Args:
            toolbar_name (str):
            item_name (str):

        Returns:
            QWidget|QAction
        """
        return ToolBarRegistry.get_toolbar_item(toolbar_name, item_name)

    @staticmethod
    def get_toolbar_items(toolbar_name: str, *item_names: str) -> list[Union[QWidget, QAction]]:
        """
        Get toolbar items

        Args:
            toolbar_name (str):
            item_names (tuple[str]):
        Returns:
            list[QWidget|QAction]
        """
        return ToolBarRegistry.get_toolbar_items(toolbar_name, *item_names)

    @staticmethod
    def get_toolbar(toolbar_name: str) -> PieToolBar:
        """
        Get toolbar by its name
        """
        return ToolBarRegistry.get_toolbar(toolbar_name)

    @staticmethod
    def get_toolbars(*toolbar_names: str) -> list[PieToolBar]:
        """
        Get toolbars by its names
        """
        return ToolBarRegistry.get_toolbars(*toolbar_names)
