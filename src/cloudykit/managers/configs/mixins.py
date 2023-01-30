import typing

from cloudykit.system.manager import System
from cloudykit.managers.configs.manager import ConfigManager


class ConfigMixin:
    """
    Config mixin
    """

    def __init__(self, section: str) -> None:
        self._section = section
        self._config: ConfigManager = System.registry.configs

    def get(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._config.get(self._section, key, default)

    def set(self, key: typing.Any, data: typing.Any) -> None:
        self._config.set(self._section, key, data)

    def delete(self, key: typing.Any) -> None:
        self._config.delete(self._section, key)

    @property
    def config(self) -> ConfigManager:
        return self._config
