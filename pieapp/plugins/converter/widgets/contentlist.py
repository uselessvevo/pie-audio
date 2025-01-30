from PySide6.QtCore import Signal
from __feature__ import snake_case

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QAbstractItemView


class ContentListWidget(QListWidget):
    sig_item_changed = Signal()
    sig_item_deleted = Signal()
    sig_item_pressed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.set_contents_margins(0, 0, 0, 0)

        self.set_focus_policy(Qt.FocusPolicy.NoFocus)
        self.set_size_policy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.set_selection_behavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.set_selection_mode(QAbstractItemView.SelectionMode.SingleSelection)

        self.itemChanged.connect(self.sig_item_changed)
        self.itemPressed.connect(self.sig_item_pressed)
        self.model().rowsRemoved.connect(self.sig_item_deleted)
