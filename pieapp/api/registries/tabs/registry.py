from PySide6.QtWidgets import QWidget

from pieapp.api.exceptions import PieError
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry

from pieapp.widgets.toolbars.tabs import PieTab


class TabRegistryClass(BaseRegistry):
    name = SysRegistry.Tabs

    def init(self) -> None:
        self._tabs = {}
        self._tabs_items = {}

    def add_tab(self, tab_name: str, tab_widget: PieTab) -> PieTab:
        if tab_name in self._tabs:
            raise PieError(f"Tab {tab_name} already registered")

        self._tabs[tab_name] = tab_widget
        return tab_widget

    def get_tab(self, tab_name: str) -> PieTab:
        if tab_name not in self._tabs:
            raise PieError(f"Tab {tab_name} not found")

        return self._tabs[tab_name]

    def add_tab_item(self, tab_name: str, item_name: str, item_widget: QWidget) -> QWidget:
        # if tab_name not in self._tabs:
        #     raise PieException(f"Tab {tab_name} not found")
        #
        # if item_name in self._tabs_items:
        #     raise PieException(f"Tab item {item_name} is already registered found")
        #
        if tab_name not in self._tabs_items:
            self._tabs_items[tab_name] = {}

        self._tabs_items[tab_name][item_name] = item_widget

        return item_widget

    def get_tab_item(self, tab_name: str, item_name: str) -> QWidget:
        if tab_name not in self._tabs:
            raise PieError(f"Tab {tab_name} not found")

        if item_name not in self._tabs_items[tab_name]:
            raise PieError(f"Tab item {item_name} not found")

        return self._tabs_items[tab_name][item_name]


TabRegistry = TabRegistryClass()
