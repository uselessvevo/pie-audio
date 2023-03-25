import os
import typing

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QLabel,
    QComboBox, QLineEdit, QPushButton,
    QGridLayout, QWidget, QTabBar, QFrame,
    QFileDialog, QStylePainter, QStyleOptionTab, QStyle
)

from pieapp.structs.containers import Containers
from pieapp.structs.menus import Menus, MenuItems
from piekit.managers.menus.mixins import MenuAccessor
from piekit.managers.plugins.decorators import onPluginAvailable
from piekit.managers.registry import Managers
from piekit.managers.structs import Sections, SysManagers
from piekit.managers.toolbars.mixins import ToolBarAccessor
from piekit.managers.toolbuttons.mixins import ToolButtonAccessor
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor
from piekit.system.loader import Config
from piekit.utils.files import writeJson


class HorizontalTabBar(QTabBar):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QTabBar::tab {width: 100%}")

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(
                self.tabRect(index),
                QtCore.Qt.AlignCenter | QtCore.Qt.TextDontClip,
                self.tabText(index)
            )

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        if size.width() < size.height():
            size.transpose()
        return size


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.setTabBar(HorizontalTabBar())


class Spacer(QFrame):

    def __init__(self, frameLine: bool = False):
        super(Spacer, self).__init__()
        if frameLine:
            self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)


class MainSettingsWidget(
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    QWidget
):
    section = Sections.Shared

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        mainGrid = QGridLayout(parent)

        self.ffmpegPrompt = QLineEdit()
        self.ffmpegPrompt.insert(self.getConfig("ffmpeg.root", section=Sections.User))
        self.ffmpegButton = QPushButton(self.getTranslation("Set ffmpeg path"))
        self.ffmpegButton.clicked.connect(self.ffmpegButtonConnect)

        locales = Config.LOCALES
        self.localeCBox = QComboBox()
        self.localeCBox.addItems(locales)
        self.localeCBox.setCurrentText(self.getConfig("locales.locale", Config.DEFAULT_LOCALE, section=Sections.User))

        themes = Managers(SysManagers.Assets).themes
        self.themeCBox = QComboBox()
        self.themeCBox.addItems(themes)
        self.themeCBox.setCurrentText(self.getConfig("theme", section=Sections.User))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        mainGrid.addWidget(QLabel(self.getTranslation("Language")), 0, 0, 1, 1)
        mainGrid.addWidget(self.localeCBox, 0, 1, 1, 1)

        mainGrid.addWidget(QLabel(self.getTranslation("Theme")), 2, 0, 1, 1)
        mainGrid.addWidget(self.themeCBox, 2, 1, 1, 1)

        mainGrid.addWidget(QLabel(self.getTranslation("FFmpeg path")), 6, 0, 1, 1)
        mainGrid.addWidget(self.ffmpegPrompt, 6, 1, 1, 1)
        mainGrid.addWidget(self.ffmpegButton, 7, 1, 1, 1)
        mainGrid.setAlignment(self.ffmpegButton, Qt.AlignRight)
        mainGrid.addWidget(Spacer(), 8, 0, 1, 2)

        self.setLayout(mainGrid)

    def ffmpegButtonConnect(self) -> None:
        directory = QFileDialog(self, self.getTranslation("Select ffmpeg directory"))
        directory.setFileMode(QFileDialog.DirectoryOnly)
        directory.setOption(QFileDialog.ShowDirsOnly, False)
        directory.getExistingDirectory(self, directory=str(Config.USER_ROOT))
        directoryPath = directory.directory().path()

        if directoryPath:
            writeJson(
                file=str(Config.USER_ROOT / Config.USER_CONFIG_FOLDER / "ffmpeg.json"),
                data={"root": directoryPath},
                create=True
            )
            self.ffmpegPrompt.setText(directoryPath)


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
        self.dialog = QDialog(self.parent())
        self.dialog.setWindowTitle(self.getTranslation("Settings"))
        self.dialog.setWindowIcon(self.getAssetIcon("settings.png"))
        self.dialog.resize(740, 450)

        rootGrid = QGridLayout(self.dialog)

        tabWidget = QTabWidget(self.dialog)
        tabWidget.setTabBar(HorizontalTabBar())
        tabWidget.setTabPosition(tabWidget.West)
        tabWidget.setDocumentMode(True)
        tabWidget.setElideMode(Qt.ElideLeft)
        tabWidget.setUsesScrollButtons(True)

        tabWidget.addTab(MainSettingsWidget(), self.getTranslation("Main"))

        rootGrid.addWidget(tabWidget, 0, 0, 1, 2)
        self.dialog.setLayout(rootGrid)

    @onPluginAvailable(target=Containers.MenuBar)
    def onMenuBarAvailable(self) -> None:
        self.addMenuItem(
            section=Sections.Shared,
            menu=Menus.File,
            name="settings",
            text=self.getTranslation("Settings"),
            triggered=self.dialog.show,
            icon=self.getAssetIcon("settings.png"),
            before=MenuItems.Exit
        )


def main(*args, **kwargs) -> typing.Any:
    return Settings(*args, **kwargs)
