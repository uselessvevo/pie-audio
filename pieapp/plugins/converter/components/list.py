from __feature__ import snake_case

from PySide6.QtWidgets import QListWidget, QSizePolicy


class ConvertListWidget(QListWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.set_object_name("ConverterList")
        self.set_contents_margins(0, 0, 0, 0)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
