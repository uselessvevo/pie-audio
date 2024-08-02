from PySide6.QtWidgets import QStyledItemDelegate


class ReadOnlyDelegate(QStyledItemDelegate):

    def create_editor(self, parent, option, index) -> None:
        return