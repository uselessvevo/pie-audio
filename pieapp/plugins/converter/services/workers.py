import os
import shutil
import uuid

import ffmpeg
from pathlib import Path
from dotty_dict import Dotty

from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtCore import QRunnable

from pieapp.api.models.media import Codec
from pieapp.api.models.media import FileInfo
from pieapp.api.models.media import Metadata
from pieapp.api.models.media import MediaFile
from pieapp.api.models.media import AlbumCover

from pieapp.helpers.ffmpeg import get_cover_album
from pieapp.helpers.logger import logger


class ConverterSignals(QObject):
    started = Signal()
    completed = Signal(list)
    failed = Signal(Exception)


class CopyFilesSignals(QObject):
    started = Signal()
    completed = Signal()
    failed = Signal(Exception)


class CopyFilesWorker(QRunnable):

    def __init__(self, selected_files: list[Path], destination: Path) -> None:
        self._signals = CopyFilesSignals()
        self._selected_files = selected_files
        self._destination = destination
        super(CopyFilesWorker, self).__init__()

    @property
    def signals(self) -> CopyFilesSignals:
        return self._signals

    def _wait_files_to_copy(self) -> None:
        files_ready: bool = False
        while not files_ready:
            if all([i.exists() for i in self._selected_files]):
                files_ready = True

        # QTimer.single_shot(500, lambda: self._wait_files_to_copy(self._files))
        self._signals.completed.emit()

    @Slot()
    def run(self) -> None:
        self._signals.started.emit()
        for index, file in enumerate(self._selected_files):
            try:
                shutil.copy2(str(file), str(self._destination))
                self._selected_files[index] = self._destination / file.name
            except Exception as e:
                self._signals.failed.emit(e)

        self._wait_files_to_copy()


class ConverterProbeWorker(QRunnable):

    def __init__(
        self,
        media_files: list[MediaFile],
        temp_folder: Path,
        ffmpeg_cmd: Path,
        ffprobe_cmd: Path,
    ) -> None:
        super().__init__()

        self._media_files = media_files
        self._temp_folder = temp_folder
        self._ffmpeg_cmd = ffmpeg_cmd
        self._ffprobe_cmd = ffprobe_cmd
        self._signals = ConverterSignals()

    @property
    def signals(self) -> ConverterSignals:
        return self._signals

    @Slot()
    def run(self) -> None:
        """
        Run ffprobe and get file information
        """
        try:
            self._signals.started.emit()
            probe_results: list[MediaFile] = []
            for media_file in self._media_files:
                probe_result = Dotty(ffmpeg.probe(media_file.path.as_posix(), self._ffprobe_cmd.as_posix()))
                album_cover_path = get_cover_album(self._ffmpeg_cmd, media_file.path, self._temp_folder)
                album_cover = AlbumCover(
                    image_path=album_cover_path,
                    image_file_format=album_cover_path.stem,
                )

                if probe_result:
                    probe_result["stream"] = probe_result["streams"][0]
                    probe_result.pop("streams")
                    metadata = Metadata(
                        title=probe_result.get("format.tags.title"),
                        genre=probe_result.get("format.tags.genre"),
                        subgenre=probe_result.get("format.tags.subgenre"),
                        track_number=probe_result.get("format.tags.track_number"),
                        featured_artist=probe_result.get("format.tags.album"),
                        primary_artist=probe_result.get("format.tags.album_artist"),
                        album_cover=album_cover
                    )
                    codec = Codec(
                        name=probe_result.get("stream.codec_name"),
                        type=probe_result.get("stream.codec_type"),
                        long_name=probe_result.get("format.codec_long_name")
                    )
                    info = FileInfo(
                        filename=os.path.basename(probe_result.get("format.filename")),
                        file_format=probe_result.get("format.format_name"),
                        bit_rate=probe_result.get("stream.bit_rate"),
                        bit_depth=probe_result.get("stream.bit_per_sample"),
                        sample_rate=probe_result.get("stream.sample_rate"),
                        duration=probe_result.get("stream.duration_ts"),
                        channels=probe_result.get("stream.channels"),
                        channels_layout=probe_result.get("stream.channel_layout"),
                        codec=codec,
                    )
                    media_file.uuid = str(uuid.uuid4())
                    media_file.info = info
                    media_file.metadata = metadata
                    probe_results.append(media_file)

            self._signals.completed.emit(probe_results)

        except ffmpeg.Error as e:
            logger.debug(e.stderr)
            self._signals.failed.emit(e)
            raise e
