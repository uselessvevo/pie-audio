from __feature__ import snake_case

import sys
import traceback

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QApplication, QMessageBox


def ErrorWindow(message):
    # TODO: Get rid of this BS QMessageBox
    app = QApplication.instance()
    app.set_quit_on_last_window_closed(True)
    app.set_window_icon(app.style().standard_icon(QStyle.StandardPixmap.SP_MessageBoxWarning))

    message_box = QMessageBox()
    message_box.finished.connect(lambda _: app.quit)
    message_box.set_window_icon(
        QApplication.style().standard_icon(QStyle.StandardPixmap.SP_MessageBoxCritical)
    )
    message_box.set_window_title("Pie-Audio. Critical error occurred")
    message_box.set_text(f"An unexpected error occurred:\n```\n{message}\n```")
    message_box.set_text_format(Qt.TextFormat.MarkdownText)
    message_box.show()

    sys.exit(app.exec())


def exception_hook(exc_type, exc_value, exc_traceback):
    message = "\n".join(["".join(traceback.format_tb(exc_traceback)), f"{exc_type.__name__}: {exc_value}"])
    ErrorWindow(message)
