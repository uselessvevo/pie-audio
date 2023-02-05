from PyQt5.QtWidgets import QWidget

from cloudykit.plugins.base import BasePlugin


class Preferences(BasePlugin, QWidget):
    name = "preferences"

    def call(self) -> None:
        pass
