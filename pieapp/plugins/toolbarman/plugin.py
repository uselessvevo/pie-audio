from __feature__ import snake_case

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QGridLayout

from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.decorators import on_plugin_available
from pieapp.api.plugins.helpers import get_plugin
from pieapp.api.plugins.plugins import PiePlugin
from pieapp.api.utils.qt import get_main_window
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.widgets.buttons import Button, ButtonRole


class ToolBarManagerPlugin(PiePlugin, ToolBarAccessorMixin):
    name = SysPlugin.ToolBarManager
    requires = [SysPlugin.ToolBarManager]


def main(parent, plugin_path):
    return ToolBarManagerPlugin(parent, plugin_path)
