import os
import ffmpeg
from pathlib import Path
from dotty_dict import Dotty

from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from PySide6.QtCore import QRunnable

from pieapp.api.structs.media import Codec
from pieapp.api.structs.media import FileInfo
from pieapp.api.structs.media import Metadata
from pieapp.api.structs.media import MediaFile
from pieapp.api.structs.media import AlbumCover

from pieapp.helpers.ffmpeg import get_cover_album
from pieapp.helpers.logger import logger


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

        self._chunk = chunk
        self._temp_folder = temp_folder
        self._ffmpeg_cmd = ffmpeg_cmd
        self._ffprobe_cmd = ffprobe_cmd

    @Slot()
    def run(self) -> None:
        """
        Run ffprobe and get file information
        """
        try:
            self.signals.started.emit()
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
            logger.critical(e.stderr)
            self.signals.failed.emit(e)
            raise e
