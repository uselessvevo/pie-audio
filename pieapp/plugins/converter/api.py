"""
ContentTable API
"""
from __feature__ import snake_case

import ffmpeg
from typing import Generator

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QRunnable, QObject, Signal, Slot, QThreadPool
from dotty_dict import Dotty

from piekit.managers.structs import Section
from piekit.plugins import PiePluginController
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from pieapp.plugins.converter.models import Metadata, FileInfo, Codec

from models import MediaFile
from piekit.utils.logger import logger


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
            probe_results: list[Dotty] = []
            for file in self._chunk:
                probe_result = ffmpeg.probe(file, self._command)
                if probe_result:
                    probe_result["stream"] = probe_result["streams"][0]
                    probe_result.pop("streams")
                    probe_results.append(Dotty(probe_result))

            self.signals.completed.emit(probe_results)

        except Exception as e:
            self._logger.critical(str(e))


class ContentTableController(
    PiePluginController,
    ConfigAccessorMixin,
    LocalesAccessorMixin,
):
    def init(self) -> None:
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

    def _get_process_result(self, chunk: list[Dotty]) -> None:
        for file_info in chunk:
            metadata = Metadata(
                title=file_info.get("format.tags.title"),
                genre=file_info.get("format.tags.genre"),
                subgenre=file_info.get("format.tags.subgenre"),
                track_number=file_info.get("format.tags.track_number"),
                featured_artist=file_info.get("format.tags.album"),
                primary_artist=file_info.get("format.tags.album_artist"),
            )
            codec = Codec(
                name=file_info.get("stream.codec_name"),
                type=file_info.get("stream.codec_type"),
                long_name=file_info.get("format.codec_long_name")
            )
            info = FileInfo(
                bit_rate=file_info.get("format.bit_rate"),
                bit_depth=file_info.get("format.bit_depth"),
                sample_rate=file_info.get("format.sample_rate"),
            )
            media_file = MediaFile(
                info=info,
                metadata=metadata
            )

    def _show_process_started(self) -> None:
        pass

    def _get_files_probe(self, chunks: tuple[str]) -> list[MediaFile]:
        models: list[MediaFile] = []
        chunks = list(self._split_by_chunks(chunks, self._chunk_size))
        pool = QThreadPool.global_instance()

        for chunk in chunks:
            worker = Worker(self._ffprobe_command, chunk)
            worker.signals.started.connect(self._show_process_started)
            worker.signals.completed.connect(self._get_process_result)
            pool.start(worker)

        return models

    def open_files(self) -> None:
        selected_files = QFileDialog.get_open_file_names(caption=self.get_translation("Open files"))
        if not selected_files:
            return

        converted_files = self._get_files_probe(selected_files[0])
        self._parent.fill_list(converted_files)
