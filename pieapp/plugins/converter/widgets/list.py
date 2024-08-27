from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QAbstractItemView


class ConverterListWidget(QListWidget):

    def __init__(
        self,
        change_callback: callable = None,
        remove_callback: callable = None
    ) -> None:
        super().__init__()
        self.set_object_name("ConverterList")
        self.set_contents_margins(0, 0, 0, 0)

        self.set_focus_policy(Qt.FocusPolicy.NoFocus)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.set_selection_behavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.set_selection_mode(QAbstractItemView.SelectionMode.SingleSelection)

        self.itemChanged.connect(change_callback)
        self.model().rowsRemoved.connect(remove_callback)

    # def item_widget(self, item: PySide6.QtWidgets.QListWidgetItem) -> PySide6.QtWidgets.QWidget:
