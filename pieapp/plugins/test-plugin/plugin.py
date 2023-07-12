from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton

from pieapp.structs.containers import Container
from pieapp.structs.menus import MainMenu
from pieapp.structs.plugins import Plugin

from piekit.config import Config
from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.managers.plugins.decorators import on_plugin_available


class TestPlugin(
    PiePlugin,
    ConfigAccessor, LocalesAccessor, AssetsAccessor,
    MenuAccessor, ToolBarAccessor, ToolButtonAccessor,
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

        call_dialog_button = self.add_tool_button(
            parent=self._dialog,
            section=f"test-plugin-toolbutton",
            name="call-dialog",
            text="Call inner dialog",
            icon=self.get_asset_icon("go.png", section=Section.Shared),
            tooltip="Call inner dialog",
            triggered=self.test_show_inner_dialog
        )
        self._toolbar = self.add_toolbar(
            parent=self._dialog,
            name=f"test-plugin-toolbar"
        )
        self.add_toolbar_item(
            section=f"test-plugin-toolbar",
            name="show-inner-dialog",
            item=call_dialog_button
        )

        self._grid_layout = QGridLayout()
        self._grid_layout.add_widget(self._toolbar, 0, 0)
        self._grid_layout.add_widget(test_plugin_info_button, 1, 0)
        self._grid_layout.add_widget(test_inner_config_button, 2, 0)
        self._grid_layout.add_widget(test_user_config_button, 3, 0)
        self._grid_layout.add_widget(ok_button, 4, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self._dialog.set_layout(self._grid_layout)

    def call(self) -> None:
        # We don't want to re-render dialog, so we're just showing it
        self._dialog.show()

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
            triggered=self.call,
            icon=self.get_plugin_icon(),
        )

        self.get_menu_bar(Section.Shared).add_menu(test_menu)

    # Test methods

    def test_show_inner_dialog(self) -> None:
        inner_dialog = QDialog(self._dialog)
        inner_dialog.set_window_title("Inner dialog")
        inner_dialog.show()

    def test_plugin_info(self) -> None:
        self.logger.debug(f"{Config.APP_ROOT=}, {Config.TEST_STR_ATTRIBUTE=}, {Config.TEST_LIST_ATTRIBUTE=}")
        self.logger.debug(self.get_asset("cancel.png"))
        self.logger.debug(self.get_plugin_icon())
        self.logger.debug(self.get_translation("Test String"))

    def test_inner_config(self) -> None:
        self.logger.debug(self.get_config("config.key1"))
        self.logger.debug("Setting new value")
        self.set_config("config.key1", "New String Value")
        self.logger.debug(self.get_config("config.key1"))

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value")
        self.logger.debug(self.get_config("config.key1"))

    def test_user_config(self) -> None:
        self.logger.debug(self.get_config("config1.key1", temp=True))
        self.logger.debug("Setting new value")
        self.set_config("config1.key1", "New String Value", temp=True)
        self.logger.debug(self.get_config("config1.key1", temp=True))

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value")
        self.logger.debug(self.get_config("config1.key1", temp=True))

        self.logger.debug("Saving data")
        self.save_config(temp=True)


def main(*args, **kwargs) -> Union[PiePlugin, None]:
    if Config.USE_TEST_PLUGIN:
        Config.APP_ROOT = 123
        Config.IMMUTABLE_FIELD = "New immutable value"
        return TestPlugin(*args, **kwargs)
