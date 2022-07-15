import os.path

from watchdog import events
from watchdog.observers import Observer

from cloudykit.abstracts.manager import IManager


class FileSystemEventHandler(events.FileSystemEventHandler):

    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name

    def on_created(self, event):
        print(f'on_created: {event=}')

    def on_closed(self, event):
        print(f'on_closed: {event=}')

    def on_moved(self, event):
        print(f'on_moved: {event=}')

    def on_deleted(self, event):
        print(f'on_deleted: {event=}')

    def on_modified(self, event):
        print(f'on_modified: {event=}')


class FileSystemObserver:

    def __init__(self):
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
        self._observer.unschedule(self._watchers.get(name))
        self._watchers.pop(name)

    @property
    def watchers(self) -> dict:
        return self._watchers
