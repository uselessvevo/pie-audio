import typing

from cloudykit.system import System
from cloudykit.managers.locales.manager import LocalesManager


class LocalesAccessor:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._locales: LocalesManager = System.registry.locales

    def get_translation(self, key: typing.Any) -> typing.Any:
        return self._locales.get(self._section, key)

    getTranslation = get_translation

    @property
    def locales(self) -> LocalesManager:
        return self._locales
