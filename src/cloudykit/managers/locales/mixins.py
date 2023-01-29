import typing

from cloudykit.system.manager import System


class LocalesMixin:
    """
    Config mixin
    """

    def get_trans(self, section: str, key: typing.Any, default: typing.Any = None) -> typing.Any:
        return System.registry.locales.get(section, key, default)
