import typing

from pieapp.structs.plugins import Plugin

from piekit.config import Config
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class TestPlugin(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = Plugin.TestPlugin
    section = Plugin.TestPlugin

    def init(self) -> None:
        self.logger.info(f"{Config.APP_ROOT=}, {Config.TEST_STR_ATTRIBUTE=}, {Config.TEST_LIST_ATTRIBUTE=}")
        self.logger.info(self.get_config("config.key"))
        self.logger.info(self.get_translation("Test String"))
        self.logger.info(self.get_asset("cancel.png"))


def main(*args, **kwargs) -> typing.Any:
    Config.APP_ROOT = 123
    Config.IMMUTABLE_FIELD = "New immutable value"
    return TestPlugin(*args, **kwargs)
