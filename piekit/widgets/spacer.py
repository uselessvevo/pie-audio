from PySide6.QtWidgets import QFrame


class Spacer(QFrame):

    def __init__(self, frame_line: bool = False):
        super(Spacer, self).__init__()
        if frame_line:
            self.set_frame_shape(QFrame.Shape.HLine)
            self.set_frame_shadow(QFrame.Shadow.Sunken)
