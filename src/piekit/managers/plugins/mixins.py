import typing

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers


class PluginsAccessor:
    """
    Config mixin
    """

    def get_plugin(self, key: typing.Any) -> typing.Any:
        return Managers.get(SysManagers.Plugins).get(key)

    getPlugin = get_plugin
