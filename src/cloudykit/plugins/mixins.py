from PyQt5 import Qt
from PyQt5 import QtWidgets


class MenuMixin:
    """ Mixin that allows create menu widget on parent """

    def createAction(
        self,
        text: str,
        icon: str,
        parent: object = None,
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


class ToolButtonMixin:
    """ Mixin that allows add toolbutton widget on parent """

    def createToolButton(self):
        pass


class ActionMixin:
    """ Mixin that allows create action on parent """

    def createAction(self):
        pass


class GenericWidgetMixin(MenuMixin, ToolButtonMixin, ActionMixin):
    pass
