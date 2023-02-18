import typing
from typing import Union

from piekit.managers.registry import Managers
from piekit.structs.etc import SharedSection
from piekit.managers.types import SysManagers


class AssetsAccessor:
    """
    Config mixin
    """

    def get_asset(
        self,
        key: typing.Any,
        default: typing.Any = None,
        section: Union[str, SharedSection] = SharedSection
    ) -> typing.Any:
        return Managers.get(SysManagers.Assets).get(self.section or section, key, default)

    getAsset = get_asset
