import typing

from cloudykit.system.manager import System


class ConfigMixin:

    def get(self, section: str, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return System.registry.config.get(section, key, default)

    def set(self, section: str, key: typing.Any, data: typing.Any) -> None:
        System.registry.config.set(section, key, data)

    def delete(self, section: str, key: typing.Any) -> None:
        System.registry.config.delete(section, key)
