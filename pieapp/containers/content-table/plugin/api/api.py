"""
ContentTable API
"""
from plugin.api.structs import ContentTableStruct
from piekit.plugins.api.api import PiePluginAPI


class ContentTableAPI(PiePluginAPI):

    def mount(self) -> None:
        fileStruct = ContentTableStruct

    def receive(self, files: list = None) -> None:
        self.parent.fillTable(files)
