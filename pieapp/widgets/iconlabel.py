from __feature__ import snake_case

from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class IconLabel(QWidget):

    def __init__(
        self,
        icon: QIcon = None,
        text: str = None,
        icon_size: tuple[int, int] = (16, 16),
        clear_timeout_msec: int = 3000,
        horizontal_spacing: int = 2,
        final_stretch: bool = True
    ) -> None:
        super(IconLabel, self).__init__()
        self._icon_size = icon_size

        layout = QHBoxLayout()
        layout.set_contents_margins(0, 0, 0, 0)
        self.set_layout(layout)

        self._timer = QTimer()
        self._timer.set_single_shot(True)
        self._timer.set_interval(clear_timeout_msec)
        self._timer.timeout.connect(self._clear_icon_label)

        self._icon_label = QLabel()
        if icon:
            self._icon_label.set_pixmap(icon.pixmap(*icon_size))

        self._label = QLabel()
        if text:
            self._label.set_text(text)

        layout.add_widget(self._icon_label)
        layout.add_spacing(horizontal_spacing)
        layout.add_widget(self._label)

        if final_stretch:
            layout.add_stretch()

    def set_icon(self, icon: QIcon) -> None:
        pixmap = icon.pixmap(*self._icon_size)
        self._icon_label.set_pixmap(pixmap)

    def set_text(self, text: str) -> None:
        self._label.set_text(text)

    def start_clear_timer(self, msec: int = None) -> None:
        if msec is not None:
            self._timer.set_interval(msec)
        if not self._timer.is_active():
            self._timer.start()

    def _clear_icon_label(self) -> None:
        self._label.clear()
        self._icon_label.clear()
