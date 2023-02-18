import typing

from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers


class PluginsAccessor:
    """
    Config mixin
    """

    def get_object(self, key: typing.Any) -> typing.Any:
        return Managers.get(SysManagers.Objects).get(key)

    getObject = get_object
