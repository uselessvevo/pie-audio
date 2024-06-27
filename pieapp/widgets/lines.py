from __feature__ import snake_case

from PySide6.QtWidgets import QFrame


class HLine(QFrame):

    def __init__(self, parent, width: int = 1) -> None:
        super().__init__(parent)
        self.set_frame_shape(QFrame.Shape.HLine)
        self.set_frame_shadow(QFrame.Shadow.Sunken)
        self.set_line_width(width)
