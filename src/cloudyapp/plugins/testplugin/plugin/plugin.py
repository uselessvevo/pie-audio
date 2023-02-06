from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from cloudykit.plugins.base import BasePlugin
from cloudykit.managers.plugins.decorators import onPluginAvailable


class TestPlugin(BasePlugin, QWidget):
    name = "testplugin"
    requires = ["preferences"]

    def init(self) -> None:
        self.prepareLayout()
        self.setWindowTitle(self.getTitle())

    def prepareLayout(self):
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.button = QPushButton("Click me!")
        self.button.setEnabled(False)
        self.button.clicked.connect(self.testFunction)
        layout.addWidget(self.button)

        # self.placeOn('workbench')

    def testFunction(self, event):
        self.logger.info("Button pressed")

    @onPluginAvailable(plugin="preferences")
    def onPreferencesAvailable(self) -> None:
        self.logger.info("Preferences plugin is available")
