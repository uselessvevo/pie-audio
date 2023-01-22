from pathlib import Path

from cloudykit.system.manager import System


def check_crabs(user_folder: str) -> bool:
    user_folder = Path(user_folder)
    req_files = set(System.config.USER_FOLDER_FILES)
    ex_files = set(i.name for i in user_folder.rglob("*.json"))
    return req_files == ex_files
