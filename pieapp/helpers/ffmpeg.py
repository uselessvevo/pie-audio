import os
import tarfile
import zipfile
import ffmpeg
from urllib import request
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from pieapp.api.gloader import Global
from pieapp.api.registries.locales.helpers import translate


def get_cover_album(cmd: Path, filepath: Path, temp_folder: Path) -> Path:
    cover_image_path = temp_folder / f"{filepath.stem!s}.jpg"
    (
        ffmpeg
        .input(filepath.as_posix())
        .output(cover_image_path.as_posix(), acodec="copy")
        .run_async(cmd=cmd.as_posix(), overwrite_output=True, pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    return cover_image_path


ARCHIVE_URL_NAME: dict[str, str] = {
    "nt": "ffmpeg-master-latest-win64-gpl.zip",
    "linux": "ffmpeg-master-latest-linux64-lgpl.tar.xz"
}

ARCHIVE_TYPE_NAME: dict[str, str] = {
    "nt": "zip",
    "linux": "tar.xz"
}


class DownloadWorker(QObject):
    sig_download_done = Signal(str)
    sig_unpack_ready = Signal(str)
    sig_download_progress = Signal(int)
    sig_unpack_archive_message = Signal(str)

    def __init__(self, release_url: str = None, archive_path: str = None) -> None:
        self._ffmpeg_binaries_path = str(Global.USER_ROOT / "ffmpeg")
        self._ffmpeg_build_url: str = None

        if release_url is None:
            self._ffmpeg_build_url = Global.FFMPEG_RELEASE_URL

        if isinstance(release_url, str):
            self._ffmpeg_build_url = release_url

        archive_name: str = ARCHIVE_URL_NAME[os.name]
        archive_file_type: str = ARCHIVE_TYPE_NAME[os.name]

        self._archive_path: str = os.path.join(archive_path or Global.USER_ROOT, f"ffmpeg.{archive_file_type}")
        self._ffmpeg_build_url: str = f"{self._ffmpeg_build_url}/{archive_name}"

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
        self.sig_download_done.emit(self._ffmpeg_binaries_path)
        self.sig_unpack_archive_message.emit("Done!")

        self.sig_unpack_archive_message.emit(translate("Checking files"))
        self.sig_unpack_archive_message.emit(f"{translate('All done')}!")
        self.sig_unpack_ready.emit(self._ffmpeg_binaries_path)

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
