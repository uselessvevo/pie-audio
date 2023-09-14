"""
ContentTable API
"""
from __feature__ import snake_case

import ffmpeg
import os.path
from typing import Generator
from dotty_dict import Dotty

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QRunnable, QObject, Signal, Slot, QThreadPool

from pieapp.structs.plugins import Plugin
from piekit.plugins.utils import get_plugin
from piekit.utils.logger import logger
from piekit.plugins import PiePluginAPI
from piekit.managers.structs import Section
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin

from models import MediaFile, Metadata, FileInfo, Codec


class Signals(QObject):
    started = Signal()
    completed = Signal(list)
    failed = Signal(Exception)


class Worker(QRunnable):

    def __init__(self, command: str, chunk: list[str]) -> None:
        super().__init__()

        self._chunk = chunk
        self._command = command
        self._logger = logger
        self.signals = Signals()

    @Slot()
    def run(self) -> None:
        """ Call the `subprocess.Popen` to execute ffprobe """
        try:
            probe_results: list[MediaFile] = []
            for file in self._chunk:
                probe_result = Dotty(ffmpeg.probe(file, self._command))
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
                    )
                    codec = Codec(
                        name=probe_result.get("stream.codec_name"),
                        type=probe_result.get("stream.codec_type"),
                        long_name=probe_result.get("format.codec_long_name")
                    )
                    info = FileInfo(
                        filename=os.path.basename(probe_result.get("format.filename")),
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

        except Exception as e:
            self._logger.critical(str(e))


class ConverterAPI(
    PiePluginAPI,
    ConfigAccessorMixin,
    LocalesAccessorMixin,
):
    def init(self) -> None:
        self._current_files = []
        self._chunk_size = self.get_config(
            key="ffmpeg.chunk_size",
            default=10,
            scope=Section.Root,
            section=Section.User,
        )
        self._ffprobe_command = self.get_config(
            key="ffmpeg.ffprobe",
            default="ffprobe",
            scope=Section.Root,
            section=Section.User
        )

    def _split_by_chunks(self, files: tuple[str], n: int) -> Generator:
        for i in range(0, len(files), n):
            yield files[i:i + n]

    def _worker_started(self) -> None:
        get_plugin(Plugin.StatusBar).show_message(self.get_translation("Loading files"))

    def _worker_finished(self, models_list: list[MediaFile]) -> None:
        self._parent.fill_list(models_list)
        get_plugin(Plugin.StatusBar).show_message(self.get_translation("Done loading files"))

    def open_files(self) -> None:
        selected_files = QFileDialog.get_open_file_names(caption=self.get_translation("Open files"))
        if not selected_files:
            return

        chunks = self._split_by_chunks(selected_files[0], self._chunk_size)
        pool = QThreadPool.global_instance()

        for chunk in chunks:
            filtered_chunk = [i for i in chunk if i not in self._current_files]
            self._current_files.extend(filtered_chunk)

            worker = Worker(self._ffprobe_command, filtered_chunk)
            worker.signals.started.connect(self._worker_started)
            worker.signals.completed.connect(self._worker_finished)
            pool.start(worker)
