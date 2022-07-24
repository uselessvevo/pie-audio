from typing import Iterable

from cloudykit.managers.system.manager import System
from cloudykit.utils.files import write_json


def check_crabs(user_folder: "Path") -> Iterable:
    collect = set()


def restore_crabs(user_folder: "Path", files: tuple) -> bool:
    if user_folder.exists():
        files = System.config.get('cloudykit.userconfig')
        files_objs = set(map(user_folder.joinpath, files.keys())).difference()

        for file in files_objs:
            if not file.exists():
                write_json(str(file), files.get(file.name))

        return False

    return True
