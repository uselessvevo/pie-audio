import os
import json
from typing import List, Union, Any
from pathlib import Path


def touch(file_name):
    try:
        os.utime(file_name, None)
    except OSError:
        open(file_name, 'a').close()


def read_json(file: Union[str, Path], hang_on_error: bool = True, default: bool = None, create: bool = False) -> Any:
    try:
        if create and not os.path.exists(file):
            write_json(file, {})
        with open(file, encoding='utf-8') as output:
            return json.load(output)

    except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
        if not hang_on_error:
            return default
        else:
            raise err


def write_json(file: str, data: Any, mode: str = 'w'):
    try:
        data = json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False)
        with open(file, mode, encoding='utf-8') as output:
            output.write(data)

    except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
        raise err


def update_json(file, data, create=False):
    copy = read_json(file, create=create)
    copy.update(data)
    write_json(file, copy)


# Managers

def write_folder_info(folder: Union[str, Path]) -> bool:
    written_folder_size = current_folder_size = 0
    info_file = Path(folder, 'info.json')

    # Update file if exists
    if info_file.exists():
        written_folder_size = read_json(info_file).get('size')
    else:
        # Create folder size entry
        for file in Path(folder).rglob('*.*'):
            if file.is_file():
                current_folder_size += file.stat().st_size

        update_json(info_file, {'size': current_folder_size}, create=True)

    return current_folder_size > written_folder_size


def write_assets_file(prefix, root, folder, file_formats=None, path_slice=-2):
    """
    Collect files from folder and restore manifest.json files
    Args:
        prefix (str): prefix to file (f.e. "shared/icons/icon.svg")
        folder (str): folder path
        path_slice (int): path slice
        file_formats (list|tuple): list of file formats
    Returns:
        hash table of formatted file paths (str)
    """
    folder = Path(folder)
    if not folder.exists():
        raise OSError('Path doesn\'t exit')

    file = folder.joinpath('assets.json')

    if not file_formats:
        file_formats = []

    collect = {}

    file_formats = set(f'*.{i}' for i in file_formats)
    for file_format in file_formats:
        for file in folder.rglob(file_format):
            key = f'{prefix}/{"/".join(file.parts[path_slice:])}'
            collect.update({key: str(file)})

    if not file.exists():
        write_json(file, collect)

    return collect


readJson = read_json
