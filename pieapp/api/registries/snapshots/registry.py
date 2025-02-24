from typing import Union, Any

from PySide6.QtCore import QObject, Signal

from pieapp.api.utils.logger import logger
from pieapp.api.exceptions import PieError
from pieapp.api.registries.base import BaseRegistry
from pieapp.api.registries.sysregs import SysRegistry

from pieapp.api.models.indexes import Index
from pieapp.api.converter.models import MediaFile


class SnapshotRegistryClass(QObject, BaseRegistry):
    name = SysRegistry.Snapshots

    # Emit on snapshot created
    sig_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_snapshot_modified = Signal(MediaFile)

    # Emit on inner snapshots registry restored
    sig_snapshots_restored = Signal()

    # Global snapshots

    # Emit on snapshot created
    sig_global_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_global_snapshot_deleted = Signal(MediaFile, int)

    # Emit on snapshot modified
    sig_global_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshots registry cleared
    sig_global_snapshot_restored = Signal()

    def init(self) -> None:
        # List of MediaFile models
        self._inner_snapshots: list = []

        # List of snapshot names
        self.inner_snapshots_keys: list[str] = []

        # <media file name>: <index of the version>
        self._inner_snapshot_indexes: dict[str, int] = {}

        # List of global snapshots
        self._global_snapshots: list[MediaFile] = []

        # Current global snapshot index
        self._global_snapshots_index: int = 0

        # Dictionary of local snapshots: <scope name>: <list of MediaFile models>
        self._local_snapshots: dict[str, list[MediaFile]] = {}

        # Dictionary of current local snapshot index: <scope name>: <current index>
        self._local_snapshots_index: dict[str, int] = {}

    # Global snapshots methods

    def add_global_snapshot(self, media_file: MediaFile) -> MediaFile:
        self._global_snapshots.append(media_file)
        self._global_snapshots_index = len(self._global_snapshots) - 1
        logger.debug(f"File {media_file.name} added")
        self.sig_global_snapshot_created.emit(media_file)
        return media_file

    def get_global_snapshot(self, index: int, default: Any = None) -> MediaFile:
        try:
            return self._global_snapshots[index]
        except IndexError:
            return default

    def get_global_snapshot_index(self) -> int:
        return self._global_snapshots_index

    def update_global_snapshot_index(self, shift: int) -> tuple[MediaFile, bool]:
        """
        Update global_snapshot_index by shifting it
        """
        snapshots = self._global_snapshots
        global_index = self._global_snapshots_index + shift
        if global_index < 0:
            global_index = 0
        elif global_index > len(snapshots) - 1:
            global_index = len(snapshots) - 1

        is_array_end = False
        if global_index <= 0:
            is_array_end = True
        elif global_index >= len(snapshots) - 1:
            is_array_end = True

        self._global_snapshots_index = global_index

        return snapshots[global_index], is_array_end

    def remove_global_snapshot(self, index: int):
        del self._global_snapshots[index]
        self.sig_global_snapshot_deleted.emit(index)

    def restore_global_snapshots(self) -> None:
        self._global_snapshots = []
        self._global_snapshots_index = 0
        self.sig_global_snapshot_restored.emit()

    # Local snapshot

    def get_local_snapshot(self, name: str, index: int, default: Any = None) -> MediaFile:
        try:
            return self._local_snapshots[name][index]
        except (KeyError, IndexError):
            return default

    def get_local_snapshot_index(self, name: str) -> int:
        return self._local_snapshots_index[name]

    def add_local_snapshot(self, name: str, media_file: MediaFile) -> MediaFile:
        if name not in self._local_snapshots:
            self._local_snapshots[name] = []

        self._local_snapshots[name].append(media_file)
        self._local_snapshots_index[name] = len(self._local_snapshots[name]) - 1

        logger.debug(f"Local snapshot {media_file.name} added")
        return media_file

    def update_local_snapshot_index(self, name: str, shift: int) -> tuple[MediaFile, bool]:
        snapshots = self._local_snapshots[name]
        local_index = self._local_snapshots_index[name] + shift
        if local_index < 0:
            local_index = 0
        elif local_index > len(snapshots) - 1:
            local_index = len(snapshots) - 1

        is_array_end = False
        if local_index <= 0:
            is_array_end = True
        elif local_index >= len(snapshots) - 1:
            is_array_end = True

        self._local_snapshots_index[name] = local_index
        logger.debug(f"Local snapshot index {local_index} shifted")
        logger.debug(f"{is_array_end=}")

        return snapshots[local_index], is_array_end

    def contains_local(self, name: str, media_file: MediaFile = None) -> bool:
        if media_file:
            return media_file in self._local_snapshots[name]
        return name in self._local_snapshots

    def restore_local_snapshots(self, name: str = None) -> None:
        if name is None:
            self._local_snapshots = {}
            self._local_snapshots_index = {}
        else:
            self._local_snapshots[name] = []
            self._local_snapshots_index[name] = 0

    # Sync methods

    def sync_local_to_both(self, media_file_name: str) -> None:
        self.sync_local_to_global(media_file_name)
        self.sync_global_to_inner()

    def sync_local_to_global(self, media_file_name: str) -> None:
        local_index = self._local_snapshots_index[media_file_name]
        local_snapshot = self._local_snapshots[media_file_name][local_index]
        self._global_snapshots.append(local_snapshot)
        if self._global_snapshots_index > 0:
            self._global_snapshots_index += 1

        self.sig_global_snapshot_modified.emit(local_snapshot)
        logger.debug("Local synced with global")

    def sync_global_to_inner(self) -> None:
        if not self._global_snapshots:
            logger.debug(f"{len(self._global_snapshots)=}")
            return

        global_index = self._global_snapshots_index
        global_snapshot = self._global_snapshots[global_index]

        inner_index = self.inner_snapshots_keys.index(global_snapshot.name)
        self._inner_snapshots[inner_index].append(global_snapshot)
        self._inner_snapshot_indexes[global_snapshot.name] = len(self._inner_snapshots[inner_index]) - 1

        self.sig_snapshot_modified.emit(global_snapshot)
        logger.debug("Global synced with inner")

    # Snapshot versions

    def add(self, media_file: MediaFile) -> None:
        """
        Add new record into registry
        """
        if media_file.name not in self.inner_snapshots_keys:
            self._inner_snapshots.append([media_file])
            self._inner_snapshot_indexes[media_file.name] = 0
            self.inner_snapshots_keys.append(media_file.name)
        else:
            raise PieError(f"File {media_file.name} is already exists")

        self.sig_snapshot_created.emit(media_file)
        logger.debug(f"File {media_file.name} added")

    def get(self, name: str, version: int = None) -> Union[list[MediaFile], MediaFile]:
        logger.debug(f"Snapshot {name}:{version}")
        logger.debug(self.inner_snapshots_keys)
        if name not in self.inner_snapshots_keys:
            return
            # raise PieException(f"File with \"{name}\" was not found")

        index = self.inner_snapshots_keys.index(name)
        snapshots = self._inner_snapshots[index]
        if version:
            return snapshots[version]
        else:
            cur_index = self._inner_snapshot_indexes[name]
            return snapshots[cur_index]

    def update(self, name: str, new_media_file: MediaFile, version: int = None) -> None:
        logger.debug(f"Snapshot {name} was updated to {new_media_file}:{version}")
        if name not in self.inner_snapshots_keys:
            return
            # raise PieException(f"File with \"{name}\" was not found")

        index = self.inner_snapshots_keys.index(name)
        snapshots = self._inner_snapshots[index]
        if version:
            snapshots[version] = new_media_file
        else:
            snapshots.append(new_media_file)

        self.sig_snapshot_modified.emit(new_media_file)

    def remove(self, name: str, version: int = None) -> None:
        logger.debug(f"Removing snapshot {name}:{version}")
        if name not in self.inner_snapshots_keys:
            return

        index = self.inner_snapshots_keys.index(name)
        snapshots = self._inner_snapshots[index]
        if version:
            self.sig_snapshot_deleted.emit(snapshots[name][version:Index.End])
            del snapshots[name][version:Index.End]
        else:
            self.sig_snapshot_deleted.emit(self._inner_snapshots[index][Index.End])
            del self._inner_snapshots[index]
            del self.inner_snapshots_keys[index]

        logger.debug(f"Snapshot {name}:{version} was removed")

    def contains(self, name: MediaFile) -> bool:
        return name in self.inner_snapshots_keys

    def values(self, as_path: bool = False) -> list[Any]:
        return [i[-1].path if as_path else i[-1] for i in self._inner_snapshots]

    def count(self) -> int:
        return len(self._inner_snapshots)

    def index(self, name: str) -> int:
        return list(self.inner_snapshots_keys).index(name)

    def restore(self) -> None:
        self._inner_snapshots = []
        self.inner_snapshots_keys = []
        self._inner_snapshot_indexes = {}
        self._global_snapshots = []
        self._global_snapshots_index = 0
        self._local_snapshots = {}
        self._local_snapshots_index = {}
        self.sig_snapshots_restored.emit()
        self.sig_global_snapshot_restored.emit()
        logger.debug("Snapshots restored")


SnapshotRegistry = SnapshotRegistryClass()
