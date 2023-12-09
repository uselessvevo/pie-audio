from __feature__ import snake_case

from watchdog import events
from watchdog.observers import Observer

from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from piekit.exceptions import PieException
from piekit.globals import Global
from piekit.managers.locales.utils import translate
from piekit.utils.logger import logger


class FileSystemEventHandler(QObject, events.FileSystemEventHandler):
    sig_file_moved = Signal(str, str, bool)
    sig_file_created = Signal(str, bool)
    sig_file_deleted = Signal(str, bool)
    sig_file_modified = Signal(str, bool)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        events.FileSystemEventHandler.__init__(self)

    @staticmethod
    def format_is_directory(is_directory: bool) -> str:
        return "directory" if is_directory else "file"

    def on_moved(self, event):
        source_path = event.src_path
        destination_path = event.dest_path
        is_directory = event.is_directory
        logger.info("Moved {0}: {1} to {2}".format(
            self.format_is_directory(is_directory), source_path, destination_path)
        )
        self.sig_file_moved.emit(source_path, destination_path, is_directory)

    def on_created(self, event):
        source_path = event.src_path
        is_directory = event.is_directory
        logger.info("Created {0}: {1}".format(
            self.format_is_directory(is_directory), source_path)
        )
        self.sig_file_created.emit(source_path, is_directory)

    def on_deleted(self, event):
        source_path = event.src_path
        is_directory = event.is_directory
        logger.info("Deleted {0}: {1}".format(
            self.format_is_directory(is_directory), source_path)
        )
        self.sig_file_deleted.emit(source_path, is_directory)

    def on_modified(self, event):
        source_path = event.src_path
        is_directory = event.is_directory
        logger.info("Modified {0}: {1}".format(
            self.format_is_directory(is_directory), source_path)
        )
        self.sig_file_modified.emit(source_path, is_directory)


class FileSystemWatcher(QObject):
    observer = None

    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)
        self._event_handler = FileSystemEventHandler(self)

    @property
    def event_handler(self) -> FileSystemEventHandler:
        return self._event_handler

    def connect_signals(self, target: QObject):
        self._event_handler.sig_file_created.connect(target.file_created)
        self._event_handler.sig_file_moved.connect(target.file_moved)
        self._event_handler.sig_file_deleted.connect(target.file_deleted)
        self._event_handler.sig_file_modified.connect(target.file_modified)

    def start(self, folder: str) -> None:
        try:
            self.observer = Observer()
            self.observer.schedule(
                event_handler=self._event_handler,
                path=folder,
                recursive=True
            )
            try:
                self.observer.start()
            except OSError as e:
                logger.critical(f"Watcher could not be started: {e!s}")
        except OSError as e:
            self.observer = None
            if "inotify" in str(e):
                QMessageBox.warning(
                    parent=self.parent(),
                    title=Global.PIEAPP_APPLICATION_NAME,
                    text=translate(
                        "Please, use this command `sudo sysctl -n -w fs.inotify.max_user_watches=524288` "
                        "to fix the issue with file system can't handle too many files in the directory."
                        "After doing that, you need to close and start the program again"
                    )
                )
            else:
                raise PieException(str(e))

    def stop(self) -> None:
        if self.observer is not None:
            try:
                self.observer.stop()
                self.observer.join()
                del self.observer
                self.observer = None
            except RuntimeError as e:
                logger.critical(f"An error has been occurred while stopping observer: {e!s}")
