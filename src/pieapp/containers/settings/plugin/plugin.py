import typing

from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class Settings(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "settings"

    def init(self) -> None:
        pass


def main(*args, **kwargs) -> typing.Any:
    return Settings(*args, **kwargs)
