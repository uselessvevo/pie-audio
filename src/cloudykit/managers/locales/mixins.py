import typing

from cloudykit.system.manager import System
from cloudykit.managers.locales.manager import LocalesManager


class LocalesMixin:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._locales: LocalesManager = System.registry.locales

    def get(self, key: typing.Any) -> typing.Any:
        return self._locales.get(self._section, key)

    def set(self, key: typing.Any, data: typing.Any) -> None:
        self._locales.set(self._section, key, data)

    def delete(self, key: typing.Any) -> None:
        self._locales.delete(self._section, key)

    @property
    def locales(self) -> LocalesManager:
        return self._locales
