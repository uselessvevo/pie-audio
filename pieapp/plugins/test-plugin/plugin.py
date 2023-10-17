import uuid
from typing import Union

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton

from pieapp.structs.layouts import Layout
from pieapp.structs.menus import MainMenu
from pieapp.structs.plugins import Plugin
from pieapp.structs.workbench import WorkbenchItem

from piekit.globals import Global
from piekit.utils.logger import logger
from piekit.managers.structs import Section
from piekit.plugins.plugins import PiePlugin
from piekit.managers.base import BaseManager
from piekit.managers.registry import Managers
from piekit.plugins.mixins import ContainerRegisterMixin
from piekit.managers.menus.mixins import MenuAccessorMixin
from piekit.managers.icons.mixins import IconAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.toolbars.mixins import ToolBarAccessorMixin
from piekit.managers.layouts.mixins import LayoutsAccessorMixin
from piekit.managers.toolbuttons.mixins import ToolButtonAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_event
from piekit.widgets.spacer import Spacer


class TestPlugin(
    PiePlugin, LayoutsAccessorMixin, ContainerRegisterMixin,
    ConfigAccessorMixin, LocalesAccessorMixin, IconAccessorMixin,
    MenuAccessorMixin, ToolBarAccessorMixin, ToolButtonAccessorMixin,
):
    """
    This plugin made to test piekit
    
    TODO: Add toolbar with tabs (ribbon) to test more stuff
    """
    
    name = Plugin.TestPlugin
    section = Plugin.TestPlugin
    requires = [Plugin.MenuBar, Plugin.Workbench]

    def init(self) -> None:
        self._dialog = QDialog(self._parent)
        self._dialog.set_modal(True)
        self._dialog.set_window_title("Test Plugin")
        self._dialog.set_window_icon(self.get_plugin_icon())
        self._dialog.resize(400, 300)

        ok_button = QPushButton(self.get_translation("Ok"))
        ok_button.clicked.connect(self._dialog.close)

        test_plugin_info_button = QPushButton("Test plugin info")
        test_plugin_info_button.clicked.connect(self.test_plugin_info)

        test_inner_config_button = QPushButton("Test restore temp config")
        test_inner_config_button.set_tool_tip("Get and set inner config")
        test_inner_config_button.clicked.connect(self.test_restore_test_config)

        test_user_config_button = QPushButton("Test save inner config")
        test_user_config_button.set_tool_tip("Get, set and save user config")
        test_user_config_button.clicked.connect(self.test_inner_config_save)

        # NOTE: You can ignore `add_toolbar`, `add_tool_button` and `add_toolbar_item`
        #       And register local toolbar and tool button
        self._toolbar = self.add_toolbar(
            parent=self._dialog,
            name=f"test-plugin-toolbar"
        )
        call_dialog_button = self.add_tool_button(
            section=f"test-plugin-toolbutton",
            name="call-dialog",
            text="Call inner dialog",
            icon=self.get_svg_icon("mood.svg", section=Section.Shared),
            tooltip="Call inner dialog",
            triggered=self.test_show_inner_dialog
        )
        self.add_toolbar_item(
            toolbar=f"test-plugin-toolbar",
            name="show-inner-dialog",
            item=call_dialog_button
        )

        self._main_layout = QGridLayout()
        self._main_layout.add_widget(self._toolbar, 0, 0)
        self._main_layout.add_widget(test_plugin_info_button, 1, 0)
        self._main_layout.add_widget(test_inner_config_button, 2, 0)
        self._main_layout.add_widget(test_user_config_button, 3, 0)
        self._main_layout.add_widget(ok_button, 5, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self._dialog.set_layout(self._main_layout)

        mw_main_layout = self.get_layout(Layout.Main)
        mw_main_layout.add_layout(self._main_layout, 0, 1, Qt.AlignmentFlag.AlignHCenter)

    def call(self) -> None:
        # We don't want to re-render dialog, so we're just showing it
        self._dialog.show()

    def register_object(self, target: "QObject", *args, **kwargs) -> None:
        self._main_layout.add_widget(target, 4, 0)

    @on_plugin_event(target=Plugin.Workbench)
    def on_workbench_available(self) -> None:
        self.add_toolbar_item(
            toolbar=Plugin.Workbench,
            name=WorkbenchItem.Spacer,
            item=Spacer()
        )
        self.add_tool_button(
            section=self.name,
            name="TestButton",
            text=self.get_translation("Test"),
            tooltip=self.get_translation("Test"),
            icon=self.get_plugin_icon(),
            triggered=self.call
        )
        self.add_toolbar_item(
            toolbar=Plugin.Workbench,
            name="test-plugin-workbench-item",
            item=self.get_tool_button(self.name, "TestButton"),
            after=WorkbenchItem.Spacer
        )

    @on_plugin_event(target=Plugin.MenuBar)
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

    def test_set_config_fields(self) -> None:
        self._logger.debug("Trying to change \"Config.APP_ROOT/IMMUTABLE_FIELD\" fields")
        Global.APP_ROOT = 123
        Global.IMMUTABLE_FIELD = "New immutable value"

    def test_show_inner_dialog(self) -> None:
        inner_dialog = QDialog(self._dialog)
        inner_dialog.set_window_title("Inner dialog")
        inner_dialog.show()

    def test_plugin_info(self) -> None:
        self.logger.debug(f"{Global.APP_ROOT=}, {Global.TEST_STR_ATTRIBUTE=}, {Global.TEST_LIST_ATTRIBUTE=}")
        self.logger.debug(self.get_icon_path("cancel.svg"))
        self.logger.debug(self.get_plugin_icon())
        self.logger.debug(self.get_translation("Test String"))

    def test_restore_test_config(self) -> None:
        self.logger.debug("Setting new value")
        self.set_config("key", "New String Value", temp=True)
        self.logger.debug(f"Value: {self.get_config('key')}")
        self.logger.debug(f"Value from temp: {self.get_config('key', temp=True)}")

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value from temp")
        self.logger.debug(self.get_config("key", temp=True))
        self.logger.debug("=================================")

    def test_inner_config_save(self) -> None:
        self.logger.debug(self.get_config("key"))
        self.logger.debug("Setting new value")
        self.set_config("key", str(uuid.uuid4()), temp=True)
        self.logger.debug(self.get_config("key", temp=True))

        self.logger.debug("Restoring configuration")
        self.restore_config()

        self.logger.debug("Retrieving value")
        self.logger.debug(self.get_config("key", temp=True))

        self.logger.debug("Saving data")
        self.save_config(temp=True)

        self.logger.debug("Retrieving saved value")
        self.logger.debug(self.get_config("key"))
        self.logger.debug(self.get_config("key", temp=True))

    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon("app.svg", section=self.name)


class TestMagicManager(BaseManager):
    name = "test-magic-manager"

    def __init__(self) -> None:
        self._logger = logger

    def init(self, *args, **kwargs) -> None:
        self._logger.debug("* Testing magic *")

    def shutdown(self, *args, **kwargs):
        self._logger.debug("No more magic...")

    def reload(self):
        self.shutdown()
        self.init()


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    Global.load_by_path(str(plugin_path / "globals.py"))

    if Global.TEST_PLUGIN_ENABLE:
        Managers.from_class(TestMagicManager)
        return TestPlugin(parent, plugin_path)
