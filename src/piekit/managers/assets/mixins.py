import typing
from typing import Union


from piekit.managers.registry import Managers
from piekit.managers.types import SysManagers, Sections


class AssetsAccessor:
    """
    Config mixin
    """

    def get_asset(
        self,
        key: typing.Any,
        default: typing.Any = None,
        section: Union[str, Sections.Shared] = Sections.Shared
    ) -> typing.Any:
        return Managers(SysManagers.Assets)(self.section or section, key, default)

    def get_asset_icon(
        self,
        key: typing.Any,
        default: typing.Any = None,
        section: Union[str, Sections.Shared] = Sections.Shared
    ):
        return Managers(SysManagers.Assets).get_icon(self.section or section, key, default)

    getAsset = get_asset
    getAssetIcon = get_asset_icon
