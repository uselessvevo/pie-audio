import typing

from cloudykit.system.manager import System
from cloudykit.managers.assets.manager import AssetsManager


class AssetsMixin:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._assets: AssetsManager = System.registry.locales

    def get(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._assets.get(self._section, key, default)

    def set(self, key: typing.Any, data: typing.Any) -> None:
        self._assets.set(self._section, key, data)

    def delete(self, key: typing.Any) -> None:
        self._assets.delete(self._section, key)

    @property
    def assets(self) -> AssetsManager:
        return self._assets
