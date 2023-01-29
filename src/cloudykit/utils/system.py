from cloudykit.system.manager import System


def check_crabs() -> bool:
    user_folder = System.user_root / System.config.CONFIGS_FOLDER
    templates_folder = System.sys_root / System.config.TEMPLATE_FOLDER
    req_files = set(i.name for i in templates_folder.rglob("*.json"))
    ex_files = set(i.name for i in user_folder.rglob("*.json"))
    return req_files == ex_files
