from pathlib import Path

from watchdog import events
from watchdog.observers import Observer

from PySide6.QtCore import Signal
from PySide6.QtCore import QObject

from pieapp.helpers.logger import logger
from pieapp.api.exceptions import PieException
from pieapp.api.registries.locales.helpers import translate


class FileSystemEventHandler(QObject, events.FileSystemEventHandler):
    sig_file_moved = Signal(Path, Path, bool)
    sig_file_created = Signal(Path, bool)
    sig_file_deleted = Signal(Path, bool)
    sig_file_modified = Signal(Path, bool)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        events.FileSystemEventHandler.__init__(self)

    @staticmethod
    def format_is_directory(is_directory: bool) -> str:
        return "directory" if is_directory else "file"

    def on_moved(self, event) -> None:
        file_path = Path(event.src_path)
        destination_path = event.dest_path
        is_directory = event.is_directory
        logger.debug("Moved {0}: {1} to {2}".format(
            self.format_is_directory(is_directory), file_path, destination_path)
        )
        self.sig_file_moved.emit(file_path, destination_path, is_directory)

    def on_created(self, event) -> None:
        file_path = Path(event.src_path)
        is_directory = event.is_directory
        logger.debug("Created {0}: {1}".format(
            self.format_is_directory(is_directory), file_path.name)
        )
        self.sig_file_created.emit(file_path, is_directory)

    def on_deleted(self, event) -> None:
        file_path = Path(event.src_path)
        is_directory = event.is_directory
        logger.debug("Deleted {0}: {1}".format(
            self.format_is_directory(is_directory), file_path.name)
        )
        self.sig_file_deleted.emit(file_path, is_directory)

    def on_modified(self, event) -> None:
        file_path = Path(event.src_path)
        is_directory = event.is_directory
        logger.debug("Modified {0}: {1}".format(
            self.format_is_directory(is_directory), file_path.name)
        )
        self.sig_file_modified.emit(file_path, is_directory)


class FileSystemWatcher(QObject):
    observer = None

    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)
        self._event_handler = FileSystemEventHandler(self)

    @property
    def events(self) -> FileSystemEventHandler:
        return self._event_handler

    def connect_signals(self, target: QObject):
        self._event_handler.sig_file_created.connect(target.on_file_created)
        self._event_handler.sig_file_moved.connect(target.on_file_moved)
        self._event_handler.sig_file_deleted.connect(target.on_file_deleted)
        self._event_handler.sig_file_modified.connect(target.on_file_modified)

    def start(self, folder: str) -> None:
        self.observer = Observer()
        self.observer.schedule(self._event_handler, folder)
        try:
            self.observer.start()
        except Exception as e:
            raise PieException(f'{translate("Can't start an observer in")} - {folder}', str(e))

    def stop(self) -> None:
        if self.observer is not None:
            try:
                self.observer.stop()
                self.observer.join()
                del self.observer
                self.observer = None
            except RuntimeError as e:
                raise PieException(translate(f"An error has been occurred while stopping observer"), str(e))
