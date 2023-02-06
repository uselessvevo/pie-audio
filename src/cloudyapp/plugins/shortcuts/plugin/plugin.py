from PyQt5.QtWidgets import QWidget

from cloudykit.plugins.base import BasePlugin


class Shortcuts(BasePlugin, QWidget):
    name = "shorcuts"

    def init(self) -> None:
        pass
