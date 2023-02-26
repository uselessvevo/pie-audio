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
    section = "test-plugin"

    def init(self) -> None:
        self.logger.info(self.getConfig("config.key"))
        self.logger.info(self.getTranslation("Test String"))
        self.logger.info(self.getAsset("cancel.png"))


def main(*args, **kwargs) -> typing.Any:
    return TestPlugin(*args, **kwargs)
