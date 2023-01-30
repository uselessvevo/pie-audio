import os
import json

from pathlib import Path
from typing import Union, Any
from json import JSONDecodeError


def touch(file_path):
    """
    Creates empty file by given path
    """
    try:
        os.utime(file_path, None)
    except OSError:
        open(file_path, 'a').close()


def read_json(
    file: Union[str, Path],
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


def write_json(file: str, data: Any, mode: str = "w", create: bool = False) -> None:
    """ Writes data in file by given path """
    try:
        if create and not os.path.exists(file):
            touch(file)

        data = json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False)
        with open(file, mode, encoding='utf-8') as output:
            output.write(data)

    except (
        OSError,
        FileNotFoundError,
        JSONDecodeError
    ) as err:
        raise err


def update_json(
    file: Union[str, Path],
    data: Any,
    create: bool = False
) -> None:
    """
    Updates file data by given path

    Args:
        file (str): file full path
        data (Any): data to update
        create (bool): creat file if it doesn't exist
    """
    copy = read_json(file, create=create)
    copy.update(data)
    write_json(file, copy)


readJson = read_json
writeJson = write_json
updateJson = update_json
