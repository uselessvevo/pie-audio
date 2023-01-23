from pathlib import Path

from cloudykit.utils.files import write_json
from cloudykit.system.manager import System


def check_crabs(user_folder: str) -> bool:
    user_folder = Path(user_folder)
    req_files = set(System.config.USER_FOLDER_FILES)
    ex_files = set(i.name for i in user_folder.rglob("*.json"))
    return req_files == ex_files


def populate_crabs(user_folder: str) -> None:
    user_folder = Path(user_folder)
    if not user_folder.exists():
        user_folder.mkdir()
        
    req_files = System.config.USER_FOLDER_FILES
    write_json(user_folder / "locales.json", {})
    write_json(user_folder / "assets.json", {})
