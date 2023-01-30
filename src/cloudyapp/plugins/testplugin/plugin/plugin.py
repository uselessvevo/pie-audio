from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from cloudykit.plugins.base import BasePlugin


class TestPlugin(BasePlugin):
    name = "testplugin"

    def mount(self) -> None:
        self.prepareButton()
        self.setWindowTitle(self.getTitle())

    def prepareButton(self):
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.testFunction)
        layout.addWidget(self.button)

        # self.placeOn('workbench')

    def testFunction(self, event):
        self.logger.info("Button pressed")
