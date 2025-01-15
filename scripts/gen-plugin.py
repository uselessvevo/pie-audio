import argparse
import shutil
import textwrap
import dataclasses as dt
from pathlib import Path


@dt.dataclass
class GenPlugin:
    name: str
    title: str
    description: str
    directory: Path


PLUGIN_SCRIPT_BODY = """
from pieapp.api.utils.logger import logger
from pieapp.api.exceptions import PieError

from pieapp.api.models.menus import MainMenu
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.models.scopes import Scope

from pieapp.api.plugins import PiePlugin
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.decorators import on_plugin_shutdown

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.registries.shortcuts.mixins import ShortcutAccessorMixin

from pieapp.api.models.themes import IconName
from pieapp.api.models.themes import ThemeProperties

# Local imports
from {PLUGIN_CLASS_NAME_LOWER}.widgets.mainwidget import {PLUGIN_CLASS_NAME}Widget


class {PLUGIN_CLASS_NAME}(
    PiePlugin, 
    ConfigAccessorMixin, 
    ThemeAccessorMixin, 
    ToolBarAccessorMixin, 
    MenuAccessorMixin,
    ShortcutAccessorMixin
):
    name = "{PLUGIN_CLASS_NAME_LOWER}"
    widget_class = {PLUGIN_CLASS_NAME}Widget
    requires = [
        SysPlugin.MainToolBar,
        SysPlugin.MainMenuBar,
        SysPlugin.ShortcutManager
    ]
    
    def get_plugin_icon(self) -> "QIcon":
        return self.get_svg_icon(IconName.App, self.name, prop=ThemeProperties.AppIconColor)

    @staticmethod
    def get_title() -> str:
        return translate("{PLUGIN_TITLE}")

    @staticmethod
    def get_description() -> str:
        return translate("{PLUGIN_DESCRIPTION}")

    def init(self) -> None:
        logger.debug(f"Hello from the %s plugin!" % self.name)
        
    @on_plugin_available(plugin=SysPlugin.MainMenuBar)
    def on_menu_bar_available(self) -> None:
        self.add_menu_item(
            scope=Scope.Shared,
            menu=MainMenu.File,
            name=self.name,
            text=self.get_title(),
            triggered=self.get_widget().call,
            icon=self.get_svg_icon(IconName.App, self.name),
        )
        
    @on_plugin_available(plugin=SysPlugin.ShortcutManager)
    def on_shortcut_manager_available(self) -> None:
        self.add_shortcut(
            name="%s_action" % self.name.lower(),
            shortcut="Ctrl+T",
            triggered=lambda: logger.debug("Hello!"),
            target=self.parent(),
            title=translate("Test me!"),
            description=translate("Print hello message")
        )

        
def main(parent, plugin_path):
    return {PLUGIN_CLASS_NAME}(parent, plugin_path)
    """


PLUGIN_WIDGET_SCRIPT_BODY = """
from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout

from pieapp.api.models.scopes import Scope
from pieapp.api.models.themes import IconName
from pieapp.api.plugins.mixins import PluginWidgetMixin

from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin

from pieapp.widgets.buttons import Button
from pieapp.widgets.buttons import ButtonRole
from pieapp.api.plugins.widgets import DialogType
from pieapp.api.plugins.widgets import PiePluginWidget


class {PLUGIN_CLASS_NAME}Widget(PiePluginWidget, PluginWidgetMixin, ThemeAccessorMixin):
    dialog_type = DialogType.Dialog

    def on_close(self) -> None:
        self.save_widget_geometry()

    def init(self) -> None:
        self.restore_widget_geometry()

        ok_button = Button(ButtonRole.Primary)
        ok_button.set_text(translate("Ok"))
        ok_button.clicked.connect(self.close)

        pixmap = QPixmap()
        icon_path = self.get_file_path(IconName.App)
        pixmap.load(icon_path)

        icon_label = QLabel()
        icon_label.set_pixmap(pixmap)

        description_label = QLabel()
        description_label.set_text("Hello!")

        grid_layout = QGridLayout()
        grid_layout.add_widget(icon_label, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(description_label, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid_layout.add_widget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.set_layout(grid_layout)

    def call(self):
        self.show()
    """


def gen_plugin(plugin_struct: GenPlugin):
    root_directory = plugin_struct.directory
    if root_directory.exists() is False:
        raise OSError(f"Plugins root directory doesn't exists: {plugin_struct.directory.parent.as_posix()}")

    plugin_directory = plugin_struct.directory / plugin_struct.name.lower()
    if plugin_directory.exists() is True:
        raise OSError(f"Plugin directory already exists: {plugin_struct.directory.as_posix()}")

    # Generate directory structure that contains essential files, directories and modules

    script_root = Path("scripts").resolve()
    plugin_directory.mkdir()
    (plugin_directory / "assets").mkdir()
    (plugin_directory / "widgets").mkdir()

    (plugin_directory / "assets" / r"dark theme").mkdir()
    (plugin_directory / "assets" / r"light theme").mkdir()

    (plugin_directory / "assets" / r"dark theme" / "icons").mkdir()
    (plugin_directory / "assets" / r"light theme" / "icons").mkdir()

    shutil.copy2(
        script_root / "app.svg",
        plugin_directory / "assets" / r"dark theme" / "icons"
    )
    shutil.copy2(
        script_root / "app.svg",
        plugin_directory / "assets" / r"light theme" / "icons"
    )

    plugin_script_body = textwrap.dedent(
        PLUGIN_SCRIPT_BODY.format(
            PLUGIN_CLASS_NAME=plugin_struct.name.title(),
            PLUGIN_CLASS_NAME_LOWER=plugin_struct.name.lower(),
            PLUGIN_TITLE=plugin_struct.title.title(),
            PLUGIN_DESCRIPTION=plugin_struct.description.title(),
        )
    )
    plugin_widget_script_body = textwrap.dedent(
        PLUGIN_WIDGET_SCRIPT_BODY.format(PLUGIN_CLASS_NAME=plugin_struct.name.title())
    )

    with open(plugin_directory / "__init__.py", "w") as _:
        pass

    with open(plugin_directory / "widgets" / "__init__.py", "w") as _:
        pass

    with open(plugin_directory / "assets" / "__init__.py", "w") as _:
        pass

    with open(plugin_directory / "assets" / r"light theme" / "__init__.py", "w") as _:
        pass

    with open(plugin_directory / "assets" / r"dark theme" / "__init__.py", "w") as _:
        pass

    with open(plugin_directory / "plugin.py", "w") as file:
        file.write(plugin_script_body)

    with open(plugin_directory / "widgets" / "mainwidget.py", "w") as file:
        file.write(plugin_widget_script_body)


parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Plugin name")
parser.add_argument("--title", help="Plugin title")
parser.add_argument("--descr", help="Plugin description")
parser.add_argument("--root", help="Full path to plugin root folders")
parsed_args = parser.parse_args()

plug_struct = GenPlugin(
    name=parsed_args.name,
    title=parsed_args.title,
    description=parsed_args.descr,
    directory=Path(parsed_args.root).resolve()
)
gen_plugin(plug_struct)
