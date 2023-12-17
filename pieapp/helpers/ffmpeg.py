import os
import subprocess

import ffmpeg
from pathlib import Path

from piekit.helpers.logger import logger


def get_cover_album(cmd: Path, filepath: Path, temp_folder: Path) -> Path:
    cover_image_path = temp_folder / f"{filepath.stem!s}.jpg"
    (
        ffmpeg
        .input(filepath.as_posix())
        .output(cover_image_path.as_posix(), acodec="copy")
        .run_async(cmd=cmd.as_posix(), overwrite_output=True, pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    return cover_image_path


def check_ffmpeg_binaries(binaries: list[Path]) -> bool:
    """
    Check if ffmpeg, ffprobe and ffplay can execute

    Args:
        binaries (tuple[Path]): Tuple of binaries paths
    """
    binaries = (f"{i}.exe" if os.name == "nt" else i for i in binaries)
    for binary in binaries:
        try:
            subprocess.Popen(binary)
        except Exception as e:
            logger.critical(e)
            return False
