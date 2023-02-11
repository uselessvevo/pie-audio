import typing

from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum


class PluginsAccessor:
    """
    Config mixin
    """

    def get_plugin(self, key: typing.Any) -> typing.Any:
        return Managers.get(SysManagersEnum.Plugins).get(key)

    getPlugin = get_plugin
