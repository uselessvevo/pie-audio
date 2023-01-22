import os.path

from watchdog import events
from watchdog.observers import Observer

from cloudykit.objects.logger import logger


class FileSystemEventHandler(events.FileSystemEventHandler):

    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name
        self._logger = logger

    def on_created(self, event):
        self._logger.info(f'on_created: {event=}')

    def on_closed(self, event):
        self._logger.info(f'on_closed: {event=}')

    def on_moved(self, event):
        self._logger.info(f'on_moved: {event=}')

    def on_deleted(self, event):
        self._logger.info(f'on_deleted: {event=}')

    def on_modified(self, event):
        self._logger.info(f'on_modified: {event=}')


class FileSystemObserver:

    def __init__(self):
        self._logger = logger
        self._watchers: dict = {}
        self._handlers: dict = {}
        self._observer: Observer = Observer()

    def mount(self) -> None:
        """ Start observer """
        self._observer.start()

    def unmount(self) -> None:
        """ Unschedule and stop observer """
        self._watchers = {}
        self._observer.unschedule_all()
        self._observer.stop()

    def reload(self):
        """ Reload all handlers """
        self._observer.unschedule_all()
        for watcher in self._watchers:
            self._observer.schedule(
                event_handler=self._watchers[watcher]['handler'],
                path=self._watchers[watcher]['path'],
            )

    def add_handler(self, path: str, name: str) -> None:
        """ Add handler by path """
        handler = FileSystemEventHandler(os.path.abspath(path))
        watcher = self._observer.schedule(handler, path)
        self._watchers[name] = {
            'handler': handler,
            'watcher': watcher,
            'path': path
        }

    def remove_handler(self, name: str) -> None:
        """ Unschedule handler by watcher name """
        watcher = self._watchers[name]['watcher']
        self._logger.info(f"Unscheduling handler for {self._watchers[name]['path']} path")
        self._observer.unschedule(watcher)
        self._watchers.pop(name)

    def remove_handlers(self, *handlers, full_house: bool = False) -> None:
        pass

    @property
    def watchers(self) -> dict:
        return self._watchers
