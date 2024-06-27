import copy
from typing import Any
from pathlib import Path

from dotty_dict import Dotty

from pieapp.helpers.logger import logger
from pieapp.helpers.files import read_json
from pieapp.helpers.files import write_json

from pieapp.api.gloader import Global
from pieapp.api.registries.models import Scope
from pieapp.api.registries.models import SysRegistry
from pieapp.api.registries.base import BaseRegistry


class ProtectedKey:
    Folder: str = "__FOLDER__"
    Temporary: str = "__TEMP__"


class ConfigRegistry(BaseRegistry):
    name = SysRegistry.Configs

    def __init__(self) -> None:
        self._configuration: Dotty = Dotty({})
        self._temp_configuration: Dotty = Dotty({})

    def init(self) -> None:
        app_root = Global.APP_ROOT / Global.CONFIGS_FOLDER_NAME
        user_root = Global.USER_ROOT / Global.CONFIGS_FOLDER_NAME / "pieapp"
        self._load_app_configs(app_root, f"{Scope.Root}.{Scope.Inner}")
        self._load_app_configs(user_root, f"{Scope.Root}.{Scope.User}")
        self._load_plugins_configs(Global.APP_ROOT / Global.PLUGINS_FOLDER_NAME)
        self._load_plugins_configs(Global.USER_ROOT / Global.CONFIGS_FOLDER_NAME)

    def _load_app_configs(self, folder: Path, scope: str) -> None:
        if folder.exists():
            config_file = folder / Global.CONFIG_FILE_NAME
            config_data = read_json(config_file, {}, True)
            config_data[ProtectedKey.Folder] = folder
            config_data[ProtectedKey.Temporary] = set()
            self._configuration[scope] = config_data

    def _load_plugins_configs(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            if (
                plugin_folder.name.startswith("__")
                or plugin_folder.name.endswith("__")
                or plugin_folder.name == "pieapp"
            ):
                continue

            # Read config in app folder - <project name>/pieapp/plugins/<plugin name>/config.json
            config_file = plugin_folder / Global.CONFIG_FILE_NAME
            config_data = read_json(config_file, {}, raise_exception=False)
            config_data[f"{plugin_folder.name}.{Scope.Inner}"] = {ProtectedKey.Folder: plugin_folder}

            # Read config in user folder - User/.pie/configs/<plugin name>/config.json
            user_plugin_folder = Global.USER_ROOT / Global.CONFIGS_FOLDER_NAME / plugin_folder.name
            user_config_file = user_plugin_folder / Global.CONFIG_FILE_NAME
            user_config_data = read_json(user_config_file, {}, raise_exception=False)
            user_config_data[f"{plugin_folder.name}.{Scope.Inner}"] = {ProtectedKey.Folder: user_plugin_folder}

            self._configuration[f"{plugin_folder.name}.{Scope.Inner}"] = {**config_data}
            self._configuration[f"{plugin_folder.name}.{Scope.User}"] = {**user_config_data}

    def get(self, scope: str, path: str, default: Any = None) -> Any:
        return self._configuration.get(f"{scope}.{path}", default=default)

    def update(self, scope: str, path: str, data: Any,
               temp: bool = False, save: bool = False, create: bool = False) -> None:
        self._configuration[f"{scope}.{path}"] = data
        if temp:
            self._configuration[f"{scope}.{ProtectedKey.Temporary}"].add(path.split(".")[0])
        if save is True:
            self.save(scope, create)

    def save(self, scope: str, create: bool = False) -> None:
        configuration_data = copy.deepcopy(self._configuration[scope])
        config_file: Path = configuration_data.get(ProtectedKey.Folder) / Global.CONFIG_FILE_NAME
        update_configuration_data = {}
        for key, value in configuration_data.items():
            if key in configuration_data[ProtectedKey.Temporary]:
                continue
            if key != ProtectedKey.Folder:
                update_configuration_data[key] = value

        update_configuration_data.pop(ProtectedKey.Temporary)
        logger.debug(f"Saving config file {config_file!s}")
        logger.debug(update_configuration_data)
        write_json(config_file, update_configuration_data, create)
