import typing

from cloudykit.system.manager import System


class ConfigMixin:
    """
    Config mixin
    """

    def __init__(self, *args, **kwargs) -> None:
        self._config = System.registry.configs

    def get(self, section: str, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return self._config.get(section, key, default)

    def set(self, section: str, key: typing.Any, data: typing.Any) -> None:
        self._config.set(section, key, data)

    def delete(self, section: str, key: typing.Any) -> None:
        self._config.delete(section, key)

    @property
    def config(self) -> "ConfigManager":
        return self.config
