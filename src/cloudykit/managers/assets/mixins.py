import typing

from cloudykit.system import System
from cloudykit.managers.assets.manager import AssetsManager


class AssetsAccessor:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._assets: AssetsManager = System.registry.assets

    def get_asset(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._assets.get(self._section, key, default)

    getAsset = get_asset

    @property
    def assets(self) -> AssetsManager:
        return self._assets
