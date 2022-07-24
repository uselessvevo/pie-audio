from PyQt5 import Qt
from PyQt5 import QtWidgets


class ManagersMixin:
    """ Managers, services mixin """

    managers = (
        'cloudykit.managers.assets.manager.AssetsManager',
        'cloudykit.managers.configs.manager.ConfigsManager',
        'cloudykit.managers.locales.manager.LocalesManager',
    )

    def mount(self) -> None:
        self.registry.mount()

    def unmount(self) -> None:
        self.registry.unmount()


class ActionMixin:
    """ Mixin that allows create menu widget on parent """

    def createAction(
        self,
        text: str,
        icon: str,
        parent: Qt.QObject = None,
        toggled: bool = False,
        shortcut: str = None,
        trigger: str = None
    ) -> QtWidgets.QAction:
        if not parent and not (hasattr(self, 'parent') or hasattr(self, '_parent')):
            parent = self

        action = QtWidgets.QAction(
            parent=parent,
            text=text,
            icon=Qt.QIcon(icon)
        )
        action.toggled = toggled
        action.setShortcut(shortcut)
        action.trigger.connect(getattr(parent, trigger))

        return action


class ToolButtonMixin:
    """ Mixin that allows add toolbutton widget on parent """

    def createToolButton(
        self,
        text: str,
        icon: str,
        parent: Qt.QObject = None,
        toggled: bool = False,
        shortcut: str = None,
        trigger: str = None
    ) -> QtWidgets.QToolButton:
        if not parent and not (hasattr(self, 'parent') or hasattr(self, '_parent')):
            parent = self

        toolbutton = QtWidgets.QToolButton(
            parent=parent
        )
        toolbutton.setText(text)
        toolbutton.setIcon(Qt.QIcon(Qt.QPixmap(icon)))
        toolbutton.setShortcut(shortcut)
        toolbutton.toggled = toggled
        toolbutton.trigger.connect(getattr(parent, trigger))

        return toolbutton


class MenuMixin:
    """ Mixin that allows create action on parent """

    def createMenu(
        self,
        text: str,
        icon: str = None,
        parent: Qt.QObject = None,
        shortcut: str = None,
        trigger: str = None
    ) -> QtWidgets.QMenu:
        if not parent and not (hasattr(self, 'parent') or hasattr(self, '_parent')):
            parent = self

        menu = QtWidgets.QMenu(parent)
        menu.addAction(f'{text} ({shortcut})', getattr(parent, trigger), shortcut=shortcut)
        menu.setIcon(Qt.QIcon(Qt.QPixmap(icon)))

        return menu
