from __feature__ import snake_case

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtGui import QCursor
from PySide6.QtGui import QAction

from PySide6.QtCore import QEvent, QRect
from PySide6.QtGui import QEnterEvent

from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QToolTip
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog

from piekit.globals import Global
from piekit.managers.locales.mixins import LocalesAccessorMixin


class ImagePreview(QToolTip):

    def __init__(self, parent, image_path: str) -> None:
        self._parent = parent
        self._string = "<img src='%s'>" % image_path if image_path else None
        super(ImagePreview, self).__init__()

    def show_tooltip(self) -> None:
        if self._string:
            self.show_text(QCursor.pos(), self._string, self._parent, QRect(), 5000)


class AlbumCoverPicker(QLineEdit, LocalesAccessorMixin):

    def __init__(
        self,
        parent=None,
        image: str = None,
        placeholder_text: str = "No image selected",
        select_album_text: str = "Select album cover image"
    ) -> None:
        super(AlbumCoverPicker, self).__init__(parent)

        self._image_path = image
        self._placeholder_text = f"<{placeholder_text}>"
        self._select_album_text = select_album_text
        self._image_preview = ImagePreview(self, self._image_path)

        self._add_image_button = QLineEdit()
        self._add_image_action = QAction()
        self._add_image_action.set_icon(self.style().standard_icon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self._add_image_action.triggered.connect(self.load_image)

        self.set_read_only(True)
        self.insert(self._image_path if self._image_path else self._placeholder_text)
        self.add_action(self._add_image_action, QLineEdit.ActionPosition.TrailingPosition)

    def enter_event(self, event: QEnterEvent) -> None:
        """
        Show tooltip with a picture miniature
        """
        self._image_preview.show_tooltip()

    def leave_event(self, event: QEvent) -> None:
        """
        Hide tooltip with a picture miniature
        """
        self._image_preview.hide_text()

    def add_image(self, image_path: str) -> None:
        self.clear()
        self.insert(image_path)

    def set_picker_icon(self, icon: QIcon) -> None:
        self._add_image_action.set_icon(icon)

    def set_load_image_method(self, method: callable) -> None:
        setattr(self, method.__qualname__, method)

    def load_image(self) -> None:
        file_path = QFileDialog.get_open_file_name(
            parent=self,
            caption=self.translate(self._select_album_text),
            dir=str(Global.USER_ROOT),
        )
        if file_path[0]:
            self.clear()
            self._image_path = Path(file_path[0])
            self.insert(self._image_path.as_posix())

    def _prepare_image(self, image: Path) -> None:
        pass
