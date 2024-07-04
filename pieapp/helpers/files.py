import os
import json
import shutil
import uuid

from pathlib import Path
from typing import Union, Any
from json import JSONDecodeError


# JSON methods


def read_json(
    file: os.PathLike,
    default: Any = None,
    create: bool = False,
    raise_exception: bool = True
) -> Any:
    """
    Read json file by given path

    Args:
        file (str): file path
        default (Any): return default value on error
        create (bool): create file if it doesn't exist
        raise_exception (bool): raise exception on error
    """
    try:
        if create and not os.path.exists(file):
            write_json(file, {})
        with open(file, encoding='utf-8') as output:
            return json.load(output)

    except (
        OSError,
        FileNotFoundError,
        JSONDecodeError
    ) as e:
        if not raise_exception:
            return default
        else:
            raise e


def write_json(file: os.PathLike, data: Any, create: bool = False) -> None:
    """
    Write data in JSON-file

    Args:
        file (os.PathLike): file name
        data (Any): data to write
        create (bool): create file if it doesn't exist
    """
    try:
        if create and not os.path.exists(file):
            create_empty_file(file)

        data = json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False)
        with open(file, "w", encoding="utf-8") as output:
            output.write(data)

    except (
        OSError,
        FileNotFoundError,
        JSONDecodeError
    ) as err:
        raise err


def update_json(file: os.PathLike, data: Any, create: bool = False) -> None:
    """
    Update JSON-file

    Args:
        file (str): file path
        data (Any): data to write
        create (bool): create file if it doesn't exist
    """
    copy = read_json(file, create=create)
    copy.update(data)
    write_json(file, copy)


def delete_files(files: list[os.PathLike]) -> None:
    """
    Delete given files

    Args:
        files (list[os.PathLike]): list of files
    """
    try:
        for file in files:
            os.remove(file)
    except OSError:
        pass


# Files and directories methods


def create_empty_file(file_path: os.PathLike):
    """
    Creates empty file by given path

    Args:
        file_path (os.PathLike): full file path
    """
    try:
        os.utime(file_path, None)
    except OSError:
        open(file_path, "a").close()


def delete_directory(directory: Union[str, os.PathLike]) -> None:
    """
    Delete directory

    Args:
        directory (os.PathLike): full
    """
    directory = Path(directory)
    if not directory.exists():
        return

    shutil.rmtree(directory)


def create_temp_directory(directory: Union[str, os.PathLike], prefix: str = None) -> Path:
    """
    Create temp directory

    Args:
        directory (str|os.PathLike): temp directory path
        prefix (str): prefix to separate directory name
    """
    temp_directory: Path = Path(directory)
    prefix_uuid: str = str(uuid.uuid4()).replace("-", "")
    if not temp_directory.exists():
        temp_directory.mkdir()

    prefix = f"{prefix}_" if prefix else ""
    temp_directory = temp_directory.joinpath(f"{prefix}{prefix_uuid}")
    if not temp_directory.exists():
        temp_directory.mkdir(exist_ok=True)

    return temp_directory
