from PySide6.QtWidgets import QWidget

from pieapp.widgets.toolbars.tabs import PieTab
from pieapp.api.registries.tabs.registry import TabRegistry


class TabBarAccessorMixin:

    @staticmethod
    def add_tab(tab_name: str, tab_title: str) -> PieTab:
        tab_bar_widget = PieTab(tab_name, tab_title)
        return TabRegistry.add_tab(tab_name, tab_bar_widget)

    @staticmethod
    def get_tab(tab_name: str) -> PieTab:
        return TabRegistry.get_tab(tab_name)

    @staticmethod
    def add_tab_item(tab_name: str, item_name: str, item_widget: QWidget,
                     after: str = None, before: str = None) -> PieTab:
        tab_widget = TabRegistry.get_tab(tab_name)
        tab_widget.add_item(tab_name, item_name, item_widget, after, before)
        return TabRegistry.add_tab_item(tab_name, item_name, item_widget)
