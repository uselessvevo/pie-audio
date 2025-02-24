from typing import Any

from pieapp.api.plugins.quickaction import QuickAction
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry


class QuickActionRegistryClass(BaseRegistry):
    name = SysRegistry.QuickAction

    def init(self) -> None:
        self._quick_actions: dict[str, object] = {}

    def add(self, quick_action: QuickAction):
        self._quick_actions[quick_action.full_name] = quick_action

    def values(self) -> list[Any]:
        return list(self._quick_actions.values())

    def restore(self) -> None:
        self._quick_actions = {}


QuickActionRegistry = QuickActionRegistryClass()
