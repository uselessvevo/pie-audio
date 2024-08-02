import ffmpeg
from pathlib import Path


def get_cover_album(cmd: Path, filepath: Path, temp_folder: Path) -> Path:
    cover_image_path = temp_folder / f"{filepath.stem!s}.jpg"
    (
        ffmpeg
        .input(filepath.as_posix())
        .output(cover_image_path.as_posix(), acodec="copy")
        .run_async(cmd=cmd.as_posix(), overwrite_output=True, pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    return cover_image_path
