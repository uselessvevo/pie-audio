from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QDialog, QGridLayout, QPushButton

from pieapp.structs.containers import Container
from pieapp.structs.menus import MainMenu
from pieapp.structs.plugins import Plugin

from piekit.config import Config
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.plugins.decorators import on_plugin_available
from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class TestPlugin(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuAccessor,
):
    name = Plugin.TestPlugin
    section = Plugin.TestPlugin
    version: str = "1.0.0"
    pieapp_version: str = "1.0.0"
    piekit_version: str = "1.0.0"
    requires = [Container.MenuBar]

    def init(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_window_title("Test Plugin")
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(400, 300)

        ok_button = QPushButton(self.get_translation("Ok"))
        ok_button.clicked.connect(self._dialog.close)

        test_plugin_info_button = QPushButton("Test plugin info")
        test_plugin_info_button.clicked.connect(self.test_plugin_info)

        test_inner_config_button = QPushButton("Test inner config")
        test_inner_config_button.set_tool_tip("Get and set inner config")
        test_inner_config_button.clicked.connect(self.test_inner_config)

        test_user_config_button = QPushButton("Test user config")
        test_user_config_button.set_tool_tip("Get, set and save user config")
        test_user_config_button.clicked.connect(self.test_user_config)

        grid_layout = QGridLayout()
        grid_layout.add_widget(test_plugin_info_button, 0, 0)
        grid_layout.add_widget(test_inner_config_button, 1, 0)
        grid_layout.add_widget(test_user_config_button, 2, 0)
        grid_layout.add_widget(ok_button, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self._dialog.set_layout(grid_layout)

    def test_plugin_info(self) -> None:
        self.logger.debug(f"{Config.APP_ROOT=}, {Config.TEST_STR_ATTRIBUTE=}, {Config.TEST_LIST_ATTRIBUTE=}")
        self.logger.debug(self.get_asset("cancel.png"))
        self.logger.debug(self.get_plugin_icon())
        self.logger.debug(self.get_translation("Test String"))

    def test_inner_config(self) -> None:
        self.logger.debug(self.get_config("config.key1", temp=True))
        self.logger.debug("Setting new value")
        self.set_config("config.key1", "New String Value", temp=True)
        self.logger.debug(self.get_config("config.key1", temp=True))

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value")
        self.logger.debug(self.get_config("config.key1", temp=True))

    def test_user_config(self) -> None:
        self.logger.debug(self.get_config("config.key1", temp=True))
        self.logger.debug("Setting new value")
        self.set_config("config1.key1", "New String Value", temp=True)
        self.logger.debug(self.get_config("config1.key1", temp=True))

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value")
        self.logger.debug(self.get_config("config1.key1", temp=True))

        self.logger.debug("Saving data")
        self.save_config(temp=True)

    @on_plugin_available(target=Container.MenuBar)
    def on_menu_bar_available(self) -> None:
        test_menu = self.add_menu(
            parent=self.get_menu_bar(Section.Shared),
            section=Section.Shared,
            name=MainMenu.Test,
            text=self.get_translation("Test"),
        )

        self.add_menu_item(
            section=Section.Shared,
            menu=MainMenu.Test,
            name="test-plugin",
            text=self.get_translation("Run test plugin"),
            triggered=self._dialog.show,
            icon=self.get_plugin_icon(),
        )

        self.get_menu_bar(Section.Shared).add_menu(test_menu)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    if Config.USE_TEST_PLUGIN:
        Config.APP_ROOT = 123
        Config.IMMUTABLE_FIELD = "New immutable value"
        return TestPlugin(*args, **kwargs)
