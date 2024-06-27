from typing import Union, Any

from pieapp.api.exceptions import PieException
from pieapp.api.models.indexes import Index
from pieapp.api.models.media import MediaFile
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.models import SysRegistry
from pieapp.helpers.logger import logger


class SnapshotRegistry(BaseRegistry):
    name = SysRegistry.Snapshots
    # TODO: Добавить в версионирование сохранение атрибутов/полей модели, а не копию модели

    def init(self) -> None:
        # <file uuid>: [MediaFile, ...]
        self._snapshots: list = []
        self._snapshots_keys: list[str] = []
        # <media file name>: <index of the version>
        self._snapshot_indexes: dict[str, int] = {}

        # Snapshots state
        self._global_snapshots: list[MediaFile] = []
        self._global_snapshot_index: int = 0

    # Global snapshots methods

    def add_global_snapshot(self, media_file: MediaFile) -> MediaFile:
        self._global_snapshots.append(media_file)
        self._global_snapshot_index = len(self._global_snapshots)
        return media_file

    def set_global_snapshot_index(self, shift: int) -> MediaFile:
        snapshots = self._global_snapshots
        global_index = self._global_snapshot_index + shift
        if global_index < 0:
            global_index = 0
        elif global_index > len(snapshots) - 1:
            global_index = len(snapshots) - 1

        self._global_snapshot_index = global_index

        result = None
        media_file = snapshots[global_index]
        index = self._snapshots_keys.index(media_file.name)
        inner_snapshots = self._snapshots[index]
        for inner_index, inner_snapshot in enumerate(inner_snapshots):
            if inner_snapshot.uuid == media_file.uuid:
                self._snapshot_indexes[inner_snapshot.name] = inner_index
                result = inner_snapshot
                logger.debug(f"Found {inner_snapshot.name}/{inner_snapshot.info.file_format}")
                logger.debug(f"{inner_snapshot.uuid=}")
                logger.debug(f"{global_index=}/{inner_index=}")

        return result

    def remove_global_snapshot(self, index: int):
        del self._global_snapshots[index]

    # Inner snapshots

    def add(self, media_file: MediaFile) -> None:
        """
        Add new record into registry
        """
        if media_file.name not in self._snapshots_keys:
            self._snapshots.append([media_file])
            self._snapshot_indexes[media_file.name] = 0
            self._snapshots_keys.append(media_file.name)
        else:
            raise PieException(f"File {media_file.name} is already exists")

        logger.debug(f"File {media_file.name} added")

    def get(self, name: str, version: int = None) -> Union[list[MediaFile], MediaFile]:
        logger.debug(f"Snapshot {name}:{version}")
        if name not in self._snapshots_keys:
            raise PieException(f"File with \"{name}\" was not found")

        index = self._snapshots_keys.index(name)
        snapshots = self._snapshots[index]
        if version:
            return snapshots[version]
        else:
            cur_index = self._snapshot_indexes[name]
            return snapshots[cur_index]

    def update(self, name: str, new_media_file: MediaFile, version: int = None) -> None:
        logger.debug(f"Snapshot {name} was updated to {new_media_file}:{version}")
        if name not in self._snapshots_keys:
            return
            # raise PieException(f"File with \"{name}\" was not found")

        index = self._snapshots_keys.index(name)
        snapshots = self._snapshots[index]
        if version:
            snapshots[version] = new_media_file
        else:
            snapshots.append(new_media_file)

    def remove(self, name: str, version: int = None) -> None:
        logger.debug(f"Snapshot {name}:{version} was removed")
        if name not in self._snapshots_keys:
            return
            # raise PieException(f"File with \"{name}\" was not found")

        index = self._snapshots_keys.index(name)
        snapshots = self._snapshots[index]
        if version:
            del snapshots[name][version:Index.End]
        else:
            del self._snapshots[index]
            del self._snapshots_keys[index]

    def contains(self, name: MediaFile) -> bool:
        return name in self._snapshots_keys

    def values(self, as_path: bool = True) -> list[Any]:
        return [i for i in self._snapshots]

    def index(self, name: str) -> int:
        return list(self._snapshots_keys).index(name)

    def restore(self) -> None:
        self._snapshots = []
        logger.debug("Snapshots restored")
