from __feature__ import snake_case

import os
import ffmpeg
from pathlib import Path
from dotty_dict import Dotty
from typing import Generator

from PySide6.QtCore import QThreadPool, QObject, Signal, QRunnable, Slot
from PySide6.QtWidgets import QFileDialog

from pieapp.structs.media import Codec
from pieapp.structs.media import FileInfo
from pieapp.structs.media import Metadata
from pieapp.structs.media import MediaFile
from pieapp.structs.media import AlbumCover
from pieapp.helpers.ffmpeg import get_cover_album
from pieapp.structs.plugins import Plugin

from piekit.globals import Global
from piekit.utils.files import create_temp_directory
from piekit.observers.filesystem import FileSystemWatcher

from piekit.utils.logger import logger
from piekit.plugins import PiePluginAPI
from piekit.plugins.utils import get_plugin
from piekit.managers.structs import Section
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin


class ConverterAPI(
    PiePluginAPI,
    ConfigAccessorMixin,
    LocalesAccessorMixin,
):
    name = Plugin.Converter

    def init(self) -> None:
        self._temp_folder: Path = None
        self._current_files: list[Path] = []
        self._watcher = FileSystemWatcher(self)

        self._chunk_size = self.get_config(
            key="ffmpeg.chunk_size",
            default=10,
            scope=Section.Root,
            section=Section.User,
        )
        self._ffmpeg_command = Path(
            self.get_config(
                key="ffmpeg.ffmpeg",
                default="ffmpeg",
                scope=Section.Root,
                section=Section.User
            )
        )
        self._ffprobe_command = Path(
            self.get_config(
                key="ffmpeg.ffprobe",
                default="ffprobe",
                scope=Section.Root,
                section=Section.User
            )
        )

    def shutdown(self) -> None:
        if self._temp_folder:
            if not self._temp_folder.exists():
                return

            for file in self._temp_folder.iterdir():
                file.unlink(missing_ok=True)
            self._temp_folder.rmdir()

    def clear_files(self) -> None:
        self._current_files = []

    def open_files(self) -> None:
        self._temp_folder = create_temp_directory(
            prefix=self.name,
            temp_directory=self.get_config(
                key="ffmpeg.temp_folder",
                default=Global.USER_ROOT / Global.DEFAULT_TEMP_FOLDER_NAME,
                scope=Section.Root,
                section=Section.User
            )
        )

        selected_files = QFileDialog.get_open_file_names(caption=self.translate("Open files"))[0]
        selected_files = list(map(Path, selected_files))
        if not selected_files:
            return

        # chunks = self._split_by_chunks(selected_files[0], self._chunk_size)
        pool = QThreadPool.global_instance()

        for index, selected_file in enumerate(selected_files):
            if selected_file not in self._current_files:
                self._current_files.append(selected_file)
            else:
                del selected_files[index]

        worker = ConverterWorker(
            chunk=selected_files,
            temp_folder=self._temp_folder,
            ffmpeg_cmd=self._ffmpeg_command,
            ffprobe_cmd=self._ffprobe_command,
        )
        worker.signals.started.connect(self._worker_started)
        worker.signals.completed.connect(self._worker_finished)
        pool.start(worker)

    # Private methods

    def _split_by_chunks(self, files: tuple[str], n: int) -> Generator:
        for i in range(0, len(files), n):
            yield files[i:i + n]

    def _worker_started(self) -> None:
        get_plugin(Plugin.StatusBar).show_message(self.translate("Loading files"))

    def _worker_finished(self, models_list: list[MediaFile]) -> None:
        self._plugin.fill_list(models_list)
        get_plugin(Plugin.StatusBar).show_message(self.translate("Done loading files"))


class Signals(QObject):
    started = Signal()
    completed = Signal(list)
    failed = Signal(Exception)
    album_cover = Signal(AlbumCover)
    metadata_ready = Signal(Metadata)


class ConverterWorker(QRunnable):

    def __init__(
        self,
        chunk: list[Path],
        temp_folder: Path,
        ffmpeg_cmd: Path,
        ffprobe_cmd: Path,
    ) -> None:
        super().__init__()

        self.signals = Signals()
        self._logger = logger

        self._chunk = chunk
        self._temp_folder = temp_folder
        self._ffmpeg_cmd = ffmpeg_cmd
        self._ffprobe_cmd = ffprobe_cmd

    def _get_cover_image(self, filename: str):
        """
        ffmpeg -i video.mp4 -map 0:v -map -0:V -c copy cover.jpg
        """
        filename_we = filename.split(".")[0]
        input_file = ffmpeg.input(filename)
        album_cover = ffmpeg.output(input_file["1"], acodec="copy", filename=f"{filename_we}.jpg")
        return album_cover

    @Slot()
    def run(self) -> None:
        """
        Run ffprobe and get file information
        """
        try:
            probe_results: list[MediaFile] = []
            for file in self._chunk:
                probe_result = Dotty(ffmpeg.probe(file.as_posix(), self._ffprobe_cmd.as_posix()))
                album_cover_path = get_cover_album(self._ffmpeg_cmd, file, self._temp_folder)
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
                    media_file = MediaFile(
                        info=info,
                        metadata=metadata
                    )
                    probe_results.append(media_file)

            self.signals.completed.emit(probe_results)

        except ffmpeg.Error as e:
            self._logger.critical(e.stderr)
            raise e
