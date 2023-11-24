from pathlib import Path
from typing import Union

import ffmpeg


ERROR_STRING_SET: set[str] = {
    "Conversion failed!",
    "Output file does not contain any stream",
}


def check_conversion_failed(error_string_set: set[str]) -> bool:
    if ERROR_STRING_SET.intersection(error_string_set):
        return False
    return True


def get_cover_album(cmd: Path, filepath: Path, temp_folder: Path) -> Path:
    cover_image_path = temp_folder / f"{filepath.stem!s}.jpg"
    (
        ffmpeg
        .input(filepath.as_posix())
        .output(cover_image_path.as_posix(), acodec="copy")
        .run_async(cmd=cmd.as_posix(), overwrite_output=True, pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    return cover_image_path
