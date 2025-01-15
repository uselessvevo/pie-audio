import copy
from typing import Any
from pathlib import Path

from dotty_dict import Dotty

from pieapp.api.utils.logger import logger
from pieapp.api.utils.files import read_json
from pieapp.api.utils.files import write_json

from pieapp.api.globals import Global
from pieapp.api.models.scopes import Scope
from pieapp.api.registries.sysregs import SysRegistry
from pieapp.api.registries.base import BaseRegistry


class ProtectedKey:
    Folder: str = "__DIR__"
    Temporary: str = "__TEMP__"


class ConfigRegistryClass(BaseRegistry):
    name = SysRegistry.Configs

    def init(self) -> None:
        self._configuration: Dotty = Dotty({})
        self._temp_configuration: Dotty = Dotty({})

        app_root = Global.APP_ROOT / Global.CONFIGS_DIR_NAME
        user_root = Global.USER_ROOT / Global.CONFIGS_DIR_NAME / "pieapp"
        self.load_app_configs(app_root, f"{Scope.Root}.{Scope.Inner}")
        self.load_app_configs(user_root, f"{Scope.Root}.{Scope.User}")
        self.load_plugins_configs(Global.APP_ROOT / Global.PLUGINS_DIR_NAME)
        self.load_plugins_configs(Global.USER_ROOT / Global.CONFIGS_DIR_NAME)

    def load_app_configs(self, folder: Path, scope: str) -> None:
        if folder.exists() is False:
            return

        for config_file in Global.APP_CONFIG_FILES:
            config_file = folder.joinpath(config_file)
            config_data = read_json(config_file, {}, True)
            config_data[ProtectedKey.Folder] = folder
            config_data[ProtectedKey.Temporary] = set()
            self._configuration[f"{scope}.{config_file.stem}"] = config_data

    def load_plugins_configs(self, plugins_folder: Path) -> None:
        if plugins_folder.exists() is False:
            return

        for plugin_folder in plugins_folder.iterdir():
            if (
                plugin_folder.name.startswith("__")
                or plugin_folder.name.endswith("__")
                or plugin_folder.name == "pieapp"
            ):
                continue

            app_plugin_folder = plugin_folder / f"{Global.CONFIG_FILE_NAME}.json"
            user_plugin_folder = Global.USER_ROOT / Global.CONFIGS_DIR_NAME / plugin_folder.name

            self._configuration[f"{plugin_folder.name}.{Scope.Inner}"] = {
                ProtectedKey.Folder: plugin_folder,
                ProtectedKey.Temporary: set()
            }
            self._configuration[f"{plugin_folder.name}.{Scope.User}"] = {
                ProtectedKey.Folder: user_plugin_folder,
                ProtectedKey.Temporary: set()
            }

            for config_file in app_plugin_folder.rglob("*.json"):
                # Read config in app folder - <project name>/pieapp/plugins/<plugin name>/<file name>.json
                config_data = read_json(config_file, {}, raise_exception=False)
                if config_file.stem in config_data:
                    del config_data[config_file.stem]
                self._configuration[f"{plugin_folder.name}.{Scope.Inner}.{config_file.stem}"] = config_data

            for user_config_file in user_plugin_folder.glob("*.json"):
                # Read config in user folder - %USER%/.pie/configs/<plugin name>/config.json
                user_config_data = read_json(user_config_file, raise_exception=True)
                if user_config_file.stem in user_config_data:
                    del user_config_data[user_config_file.stem]
                self._configuration[f"{plugin_folder.name}.{Scope.User}.{user_config_file.stem}"] = user_config_data

    def get(self, scope: str, key_path: str, default: Any = None) -> Any:
        return self._configuration.get(f"{scope}.{key_path}", default=default)

    def update(self, scope: str, path: str, data: Any,
               temp: bool = False, save: bool = False, create: bool = False) -> None:
        self._configuration[f"{scope}.{path}"] = data
        if temp:
            self._configuration[f"{scope}.{ProtectedKey.Temporary}"].add(path.split(".")[0])
        if save is True:
            # scope = ".".join(scope.split(".")[0:2])
            file_name = f"{scope.split('.')[-1]}.json"
            self.save(scope, file_name, create)

    def save(self, scope: str, file_name: str, create: bool = False) -> None:
        # Because all "root" configurations are stored in the multiple files
        parent_scope = scope
        if Scope.Root not in scope:
            parent_scope = ".".join(scope.split(".")[:-1])

        parent_scoped_data = self._configuration[parent_scope]
        plugin_directory = parent_scoped_data[ProtectedKey.Folder]
        config_data = copy.deepcopy(self._configuration[scope])
        config_file = plugin_directory / file_name
        updated_config_data = {}
        for key, value in config_data.items():
            if key in parent_scoped_data[ProtectedKey.Temporary]:
                continue
            if key != ProtectedKey.Folder:
                updated_config_data[key] = value

        if ProtectedKey.Temporary in updated_config_data:
            updated_config_data.pop(ProtectedKey.Temporary)

        if ProtectedKey.Temporary in updated_config_data:
            updated_config_data.pop(ProtectedKey.Temporary)

        logger.debug(f"Saving config file {config_file!s}")
        logger.debug(updated_config_data)
        if plugin_directory.exists() is False:
            plugin_directory.mkdir()
        write_json(config_file, updated_config_data, create)


ConfigRegistry = ConfigRegistryClass()
