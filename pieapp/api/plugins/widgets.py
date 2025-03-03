from __feature__ import snake_case

from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QDockWidget, QGridLayout, QMainWindow, QVBoxLayout


class DialogType:
    Modal = (
        Qt.WindowType.Dialog
        | Qt.WindowType.WindowSystemMenuHint
    )
    Dialog = (
        Qt.WindowType.Dialog
        | Qt.WindowType.WindowSystemMenuHint
        | Qt.WindowType.WindowCloseButtonHint
    )
    DialogMin = (
        Qt.WindowType.Dialog
        | Qt.WindowType.WindowSystemMenuHint
        | Qt.WindowType.WindowCloseButtonHint
        | Qt.WindowType.WindowMinimizeButtonHint
    )
    DialogFull = (
        Qt.WindowType.Dialog
        | Qt.WindowType.WindowSystemMenuHint
        | Qt.WindowType.WindowCloseButtonHint
        | Qt.WindowType.WindowMaximizeButtonHint
        | Qt.WindowType.WindowMinimizeButtonHint
    )


class PiePluginWidget(QWidget):
    """
    Default plugin widget/modal window
    """
    dialog_type: Qt.WindowType = None

    def __init__(self, main: QObject, plugin: "PiePlugin") -> None:
        super().__init__(main)
        self._main = main
        self._plugin = plugin
        self._name = plugin.name
        self._icon = QIcon()
        self._title = None

        if self.dialog_type is not None and isinstance(self, PieDockableWidget) is False:
            self.set_window_flags(self.dialog_type)

    def set_icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.set_window_icon(icon)

    def set_title(self, title: str) -> None:
        self._title = title
        self.set_window_title(title)

    @property
    def main(self) -> "QMainWindow":
        return self._main

    @property
    def plugin(self) -> "PiePlugin":
        return self._plugin

    @property
    def name(self) -> str:
        return self._name

    def get_main_layout(self) -> None:
        raise NotImplementedError

    def prepare(self) -> None:
        pass

    def init(self) -> None:
        pass

    def call(self) -> None:
        pass

    def on_close(self) -> None:
        pass

    def close_event(self, event):
        self.on_close()
        super().close_event(event)


class PieDockableWidget(QDockWidget):
    """
    Dockable plugin widget
    """
    dock_location = Qt.DockWidgetArea.LeftDockWidgetArea
    dock_area = Qt.DockWidgetArea.AllDockWidgetAreas
    dock_features = (QDockWidget.DockWidgetFeature.DockWidgetClosable |
                     QDockWidget.DockWidgetFeature.DockWidgetMovable)

    def __init__(self, main: QMainWindow, plugin: "PiePlugin") -> None:
        super().__init__("Dock", main)
        self._main = main
        self._plugin = plugin
        self._name = plugin.name
        self._icon = QIcon()
        self._title = None
        self._parent_layout = None

        self.set_allowed_areas(self.dock_area)
        self.set_features(self.dock_features)

        self._main_layout = QVBoxLayout()
        self._main_layout.set_spacing(0)
        self._main_layout.set_contents_margins(0, 0, 0, 0)
        self.set_layout(self._main_layout)
        self._main.add_dock_widget(self.dock_area, self)

    def set_icon(self, icon: QIcon) -> None:
        self._icon = icon
        self.set_window_icon(icon)

    def set_title(self, title: str) -> None:
        self._title = title
        self.set_window_title(title)

    def get_main_layout(self) -> QGridLayout:
        raise NotImplementedError

    @property
    def main(self) -> "QMainWindow":
        return self._main

    @property
    def plugin(self) -> "PiePlugin":
        return self._plugin

    def prepare(self) -> None:
        pass

    def init(self) -> None:
        pass

    def call(self) -> None:
        pass

    def on_close(self) -> None:
        pass

    def close_event(self, event):
        self.on_close()
        super().close_event(event)
