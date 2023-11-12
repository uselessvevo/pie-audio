from pathlib import Path

import ffmpeg


def get_cover_album(cmd: Path, filepath: Path, temp_folder: Path) -> str:
    cover_image_path = temp_folder / f"{filepath.stem!s}.jpg"
    (
        ffmpeg
        .input(filepath.as_posix())
        .output(cover_image_path.as_posix(), acodec="copy")
        .run_async(cmd=cmd.as_posix(), overwrite_output=True)
    )
    # TODO: Add timer or loop to check if file exist because ffmpeg sometimes can't get image quick
    return cover_image_path.as_posix()
