import typing

from piekit.plugins.base import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class TestPlugin(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "test-plugin"

    def init(self) -> None:
        pass


def main(*args, **kwargs) -> typing.Any:
    return TestPlugin(*args, **kwargs)
