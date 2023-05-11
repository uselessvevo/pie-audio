from __feature__ import snake_case

import typing

from PySide6.QtCore import Qt

from pieapp.structs.containers import Containers
from pieapp.structs.menus import Menus, MenuItems
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.plugins.decorators import on_plugin_available
from piekit.managers.registry import Managers
from piekit.managers.structs import Sections, SysManagers
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.config.loader import Config
from piekit.utils.files import write_json

from PySide6 import QtCore, QtWidgets


class TabBar(QtWidgets.QTabBar):

    def tab_size_hint(self, index):
        size_hint = QtWidgets.QTabBar.tab_size_hint(self, index)
        size_hint.transpose()
        return size_hint

    def paint_event(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.init_style_option(option, i)
            painter.draw_control(QtWidgets.QStyle.ControlElement.CE_TabBarTabShape, option)
            painter.save()

            rect_size = option.rect.size()
            rect_size.transpose()
            rect = QtCore.QRect(QtCore.QPoint(), rect_size)
            rect.move_center(option.rect.center())
            option.rect = rect

            tab_rect_center = self.tab_rect(i).center()
            painter.translate(tab_rect_center)
            painter.rotate(90)
            painter.translate(-tab_rect_center)
            painter.draw_control(QtWidgets.QStyle.ControlElement.CE_TabBarTabLabel, option)
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.set_tab_bar(TabBar(self))
        self.set_tab_position(QtWidgets.QTabWidget.TabPosition.West)


class Spacer(QtWidgets.QFrame):

    def __init__(self, frame_line: bool = False):
        super(Spacer, self).__init__()
        if frame_line:
            self.set_frame_shape(QtWidgets.QFrame.Shape.HLine)
            self.set_frame_shadow(QtWidgets.QFrame.Shadow.Sunken)


class MainSettingsWidget(
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    QtWidgets.QWidget
):
    name = Containers.Settings
    section = Sections.Shared

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        mainGrid = QtWidgets.QGridLayout(parent)

        self.ffpeg_prompt = QtWidgets.QLineEdit()
        self.ffpeg_prompt.insert(self.get_shared_config("ffmpeg.root", section=Sections.User))
        self.ffmpeg_button = QtWidgets.QPushButton(self.get_translation("Set ffmpeg path"))
        self.ffmpeg_button.clicked.connect(self.ffmpeg_button_connect)

        locales = Config.LOCALES
        self.locales_cbox = QtWidgets.QComboBox()
        self.locales_cbox.add_items(locales)
        self.locales_cbox.set_current_text(self.get_shared_config("locales.locale", Config.DEFAULT_LOCALE, section=Sections.User))

        themes = Managers(SysManagers.Assets).get_themes()
        self.themeCBox = QtWidgets.QComboBox()
        self.themeCBox.add_items(themes)
        self.themeCBox.set_current_text(self.get_shared_config("assets.theme", section=Sections.User))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        mainGrid.add_widget(QtWidgets.QLabel(self.get_translation("Language")), 0, 0, 1, 1)
        mainGrid.add_widget(self.locales_cbox, 0, 1, 1, 1)

        mainGrid.add_widget(QtWidgets.QLabel(self.get_translation("Theme")), 2, 0, 1, 1)
        mainGrid.add_widget(self.themeCBox, 2, 1, 1, 1)

        mainGrid.add_widget(QtWidgets.QLabel(self.get_translation("FFmpeg path")), 6, 0, 1, 1)
        mainGrid.add_widget(self.ffpeg_prompt, 6, 1, 1, 1)
        mainGrid.add_widget(self.ffmpeg_button, 7, 1, 1, 1)
        mainGrid.setAlignment(self.ffmpeg_button, Qt.AlignmentFlag.AlignRight)
        mainGrid.add_widget(Spacer(), 8, 0, 1, 2)

        self.set_layout(mainGrid)

    def ffmpeg_button_connect(self) -> None:
        directory = QtWidgets.QFileDialog(self, self.get_translation("Select ffmpeg directory"))
        directory.set_file_mode(QtWidgets.QFileDialog.FileMode.Directory)
        directory.set_option(QtWidgets.QFileDialog.Option.ShowDirsOnly, False)
        directory.get_existing_directory(self, dir=str(Config.USER_ROOT))
        directory_path = directory.directory().path()

        if directory_path:
            write_json(
                file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
                data={"root": directory_path},
                create=True
            )
            self.ffpeg_prompt.setText(directory_path)


class Settings(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    MenuAccessor,
    ToolBarAccessor,
    ToolButtonAccessor,
):
    name = Containers.Settings
    requires = [Containers.MenuBar, Containers.Workbench]

    def init(self) -> None:
        self.dialog = QtWidgets.QDialog(self.parent())
        self.dialog.set_object_name("SettingsDialog")
        self.dialog.set_window_title(self.get_translation("Settings"))
        self.dialog.set_window_icon(self.get_plugin_icon())
        self.dialog.resize(740, 450)

        rootGrid = QtWidgets.QGridLayout(self.dialog)

        tab_widget = TabWidget(self.dialog)
        tab_widget.addTab(MainSettingsWidget(), self.get_translation("Main"))

        rootGrid.add_widget(tab_widget, 0, 0, 1, 2)
        self.dialog.setLayout(rootGrid)

    @on_plugin_available(target=Containers.MenuBar)
    def on_menu_bar_available(self) -> None:
        self.addMenuItem(
            section=Sections.Shared,
            menu=Menus.File,
            name="settings",
            text=self.get_translation("Settings"),
            triggered=self.dialog.show,
            icon=self.get_asset_icon("settings.png"),
            before=MenuItems.Exit
        )


def main(*args, **kwargs) -> typing.Any:
    return Settings(*args, **kwargs)