"""
ContentTable API
"""
from piekit.config.exceptions import PieApiException
from plugin.api.structs import ContentTableStruct
from piekit.plugins.api.api import PiePluginAPI


class ContentTableAPI(PiePluginAPI):

    def init(self) -> None:
        self.file_struct = ContentTableStruct()
        self.prepare_parent_table()

    def prepare_parent_table(self) -> None:
        self.parent.set_columns(self.file_struct.count, self.file_struct.columns)

    def set_file_struct(self, file_struct: ContentTableStruct) -> None:
        if not isinstance(file_struct, ContentTableStruct):
            raise PieApiException

        self.file_struct = file_struct
        self.prepare_parent_table()

    def receive(self, files: list = None) -> None:
        self.parent.fill_table(files)
