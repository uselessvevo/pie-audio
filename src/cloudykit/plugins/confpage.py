from PyQt5 import QtWidgets

from cloudykit.plugins.base import BasePlugin


class BaseConfigPage(QtWidgets.QWidget):
    name: str

    def __init__(self, parent=None) -> None:
        if not self.name:
            raise AttributeError('Attribute `name` must be defined')

        if not isinstance(parent, BasePlugin):
            raise RuntimeError('Parent is not a `BasePlugin` based object')

        super().__init__(parent)
        self._parent = parent
        self._description = None

    def init(self) -> None:
        """ Method for widget initialization """
        raise NotImplementedError('Method `init` must be implemented')

    def refresh(self) -> None:
        """ Refresh widget method """

    def set_description(self, key: str = None, description: str = None) -> None:
        if description and key:
            raise AttributeError("Attributes `description` and `key` can't be defined together")

        if description:
            self._description = description

        if key:
            self._parent.registry.locales(
                key='Description',
                default=f'{self._parent.name.capitalize()} description'
            )

    @property
    def description(self):
        return self._description
