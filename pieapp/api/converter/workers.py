import os
import uuid
import shutil
import tarfile
import zipfile
from pathlib import Path
from urllib import request

import ffmpeg
from dotty_dict import Dotty

from PySide6.QtCore import QObject, Signal, QRunnable, Slot

from pieapp.api.converter.builders import get_query_builder
from pieapp.api.gloader import Global
from pieapp.api.converter.models import MediaFile, AlbumCover, Metadata, Codec, FileInfo
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.converter.utils import get_cover_album
from pieapp.utils.logger import logger


ARCHIVE_URL_NAME: dict[str, str] = {
    "nt": "ffmpeg-master-latest-win64-gpl",
    "linux": "ffmpeg-master-latest-linux64-lgpl"
}

ARCHIVE_TYPE_NAME: dict[str, str] = {
    "nt": "zip",
    "linux": "tar.xz"
}


class CopyFilesSignals(QObject):
    started = Signal()
    completed = Signal()
    failed = Signal(Exception)


class ConverterSignals(QObject):
    started = Signal()
    completed = Signal(list)
    failed = Signal(Exception)


class ConverterProcessSignals(QObject):
    started = Signal()
    completed_element = Signal(str)
    completed = Signal()
    failed = Signal(Exception)


class DownloadWorker(QObject):
    sig_download_done = Signal(str)
    sig_unpack_ready = Signal(str)
    sig_download_progress = Signal(int)
    sig_unpack_archive_message = Signal(str)

    def __init__(self, release_url: str = None, archive_path: str = None) -> None:
        self._ffmpeg_binaries_path = str(Global.USER_ROOT / "ffmpeg")
        self._ffmpeg_build_url: str = None

        if release_url is None:
            release_url = Global.FFMPEG_RELEASE_URL

        archive_file_type: str = ARCHIVE_TYPE_NAME[os.name]
        archive_name: str = f"{ARCHIVE_URL_NAME[os.name]}.{archive_file_type}"
        self._ffmpeg_directory = Global.USER_ROOT / "ffmpeg" / ARCHIVE_URL_NAME[os.name] / "bin"
        self._archive_path: str = os.path.join(archive_path or Global.USER_ROOT, f"ffmpeg.{archive_file_type}")
        self._ffmpeg_build_url: str = f"{release_url}/{archive_name}"

        super(DownloadWorker, self).__init__()

    def _download_progress_hook(self, block_num: int, block_size: float, total_size: float) -> None:
        read_data = block_num * block_size
        progress = read_data * 100 / total_size
        if total_size > 0:
            self.sig_download_progress.emit(progress)

    def _unpack_archive(self) -> None:
        def unpack_windows():
            zip_file = zipfile.ZipFile(self._archive_path)
            zip_file.extractall(self._ffmpeg_binaries_path)

        def unpack_linux():
            tar_file = tarfile.TarFile(self._archive_path)
            tar_file.extractall(self._ffmpeg_binaries_path)

        self.sig_unpack_archive_message.emit(f'{translate("Unpacking archive")}...')

        if os.name == "nt":
            unpack_windows()

        elif os.name == "linux":
            unpack_linux()

        os.unlink(self._archive_path)
        self.sig_download_done.emit(str(self._ffmpeg_directory))
        self.sig_unpack_archive_message.emit(f'{translate("Done")}!')

        self.sig_unpack_archive_message.emit(translate("Checking files"))
        self.sig_unpack_archive_message.emit(f"{translate('All done')}!")
        self.sig_unpack_ready.emit(str(self._ffmpeg_directory))

    def start(self) -> None:
        """
        Download latest or manually selected ffmpeg release
        and unpack archive into `BASE_DIR`
        """
        try:
            request.urlretrieve(self._ffmpeg_build_url, self._archive_path, self._download_progress_hook)
            self._unpack_archive()
        except Exception as e:
            raise e


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


class ProbeWorker(QRunnable):

    def __init__(
        self,
        media_files: list[MediaFile],
        temp_folder: Path,
        ffmpeg_command: Path,
        ffprobe_command: Path,
    ) -> None:
        super(ProbeWorker, self).__init__()

        self._media_files = media_files
        self._temp_folder = temp_folder
        self._ffmpeg_command = ffmpeg_command
        self._ffprobe_command = ffprobe_command
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
                probe_result = Dotty(ffmpeg.probe(media_file.path.as_posix(), self._ffprobe_command.as_posix()))
                album_cover_path = get_cover_album(self._ffmpeg_command, media_file.path, self._temp_folder)
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
                        file_format=media_file.path.suffix.replace(".", ""),
                        bit_rate=int(probe_result.get("stream.bit_rate")),
                        bit_depth=probe_result.get("stream.bit_per_sample"),
                        sample_rate=int(probe_result.get("stream.sample_rate")),
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


class ConverterWorker(QRunnable):

    def __init__(self, media_files: list[MediaFile], ffmpeg_command: Path) -> None:
        super(ConverterWorker, self).__init__()
        self._media_files = media_files
        self._ffmpeg_command = ffmpeg_command
        self._signals = ConverterProcessSignals()

    @property
    def signals(self) -> ConverterProcessSignals:
        return self._signals

    @Slot()
    def run(self) -> None:
        self.signals.started.emit()
        try:
            for media_file in self._media_files:
                audio_stream = ffmpeg.input(media_file.path.as_posix()).audio
                query_builder = get_query_builder(media_file)
                if not query_builder:
                    continue
                converter_query = query_builder.build()
                # output_file = (media_file.output_path.parent / f"{media_file.path.stem}.mp3").as_posix()
                audio_stream = audio_stream.output(media_file.output_path.as_posix(), **converter_query)
                ffmpeg.run(audio_stream, cmd=self._ffmpeg_command.as_posix(), overwrite_output=True)
        except Exception as e:
            print(e)
            # raise PieException(translate("Can't convert file"), str(e))
