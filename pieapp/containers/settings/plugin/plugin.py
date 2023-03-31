import typing

from PyQt6.QtCore import Qt

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

from PyQt5 import QtCore, QtWidgets


class TabBar(QtWidgets.QTabBar):

    def tabSizeHint(self, index):
        sizeHint = QtWidgets.QTabBar.tabSizeHint(self, index)
        sizeHint.transpose()
        return sizeHint

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(option, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.save()

            rectSize = option.rect.size()
            rectSize.transpose()
            rect = QtCore.QRect(QtCore.QPoint(), rectSize)
            rect.moveCenter(option.rect.center())
            option.rect = rect

            tabRectCenter = self.tabRect(i).center()
            painter.translate(tabRectCenter)
            painter.rotate(90)
            painter.translate(-tabRectCenter)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, option)
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)


class Spacer(QtWidgets.QFrame):

    def __init__(self, frameLine: bool = False):
        super(Spacer, self).__init__()
        if frameLine:
            self.setFrameShape(QtWidgets.QFrame.HLine)
            self.setFrameShadow(QtWidgets.QFrame.Sunken)


class MainSettingsWidget(
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
    QtWidgets.QWidget
):
    section = Sections.Shared

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        mainGrid = QtWidgets.QGridLayout(parent)

        self.ffmpegPrompt = QtWidgets.QLineEdit()
        self.ffmpegPrompt.insert(self.getConfig("ffmpeg.root", section=Sections.User))
        self.ffmpegButton = QtWidgets.QPushButton(self.getTranslation("Set ffmpeg path"))
        self.ffmpegButton.clicked.connect(self.ffmpegButtonConnect)

        locales = Config.LOCALES
        self.localeCBox = QtWidgets.QComboBox()
        self.localeCBox.addItems(locales)
        self.localeCBox.setCurrentText(self.getConfig("locales.locale", Config.DEFAULT_LOCALE, section=Sections.User))

        themes = Managers(SysManagers.Assets).themes
        self.themeCBox = QtWidgets.QComboBox()
        self.themeCBox.addItems(themes)
        self.themeCBox.setCurrentText(self.getConfig("theme", section=Sections.User))
        # self.themeCBox.currentIndexChanged.connect(self.themeCBoxConnect)

        mainGrid.addWidget(QtWidgets.QLabel(self.getTranslation("Language")), 0, 0, 1, 1)
        mainGrid.addWidget(self.localeCBox, 0, 1, 1, 1)

        mainGrid.addWidget(QtWidgets.QLabel(self.getTranslation("Theme")), 2, 0, 1, 1)
        mainGrid.addWidget(self.themeCBox, 2, 1, 1, 1)

        mainGrid.addWidget(QtWidgets.QLabel(self.getTranslation("FFmpeg path")), 6, 0, 1, 1)
        mainGrid.addWidget(self.ffmpegPrompt, 6, 1, 1, 1)
        mainGrid.addWidget(self.ffmpegButton, 7, 1, 1, 1)
        mainGrid.setAlignment(self.ffmpegButton, Qt.AlignRight)
        mainGrid.addWidget(Spacer(), 8, 0, 1, 2)

        self.setLayout(mainGrid)

    def ffmpegButtonConnect(self) -> None:
        directory = QtWidgets.QFileDialog(self, self.getTranslation("Select ffmpeg directory"))
        directory.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        directory.setOption(QtWidgets.QFileDialog.ShowDirsOnly, False)
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
        self.dialog = QtWidgets.QDialog(self.parent())
        self.dialog.setObjectName("SettingsDialog")
        self.dialog.setWindowTitle(self.getTranslation("Settings"))
        self.dialog.setWindowIcon(self.getAssetIcon("settings.png"))
        self.dialog.resize(740, 450)

        rootGrid = QtWidgets.QGridLayout(self.dialog)

        tabWidget = TabWidget(self.dialog)
        tabWidget.addTab(MainSettingsWidget(), self.getTranslation("Main"))
        tabWidget.addTab(MainSettingsWidget(), self.getTranslation("Main"))
        tabWidget.addTab(MainSettingsWidget(), self.getTranslation("Main"))
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
