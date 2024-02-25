import copy
from pathlib import Path
from typing import Union, Any

from dotty_dict import Dotty

from pieapp.api.globals import Global
from pieapp.api.exceptions import PieException
from pieapp.api.managers.base import BaseRegistry
from pieapp.api.managers.structs import Section
from pieapp.api.managers.structs import SysRegistry
from pieapp.helpers.files import read_json, write_json
from pieapp.helpers.logger import logger


class ConfigRegistry(BaseRegistry):
    name = SysRegistry.Configs
    protected_keys = ("__FOLDER__",)

    def __init__(self) -> None:
        self._logger = logger
        self._configuration: Dotty[str, dict[str, Any]] = Dotty({})
        self._temp_configuration: Dotty[str, dict[str, Any]] = Dotty({})

    def init(self) -> None:
        # Read app/core configurations
        self._load_app_configs(Global.APP_ROOT / Global.CONFIGS_FOLDER, Section.Inner)
        self._load_app_configs(Global.USER_ROOT / Global.CONFIGS_FOLDER, Section.User)
        self._load_plugins_configs(Global.APP_ROOT / Global.PLUGINS_FOLDER)
        self._load_plugins_configs(Global.APP_ROOT / Global.PLUGINS_FOLDER)

    def _load_app_configs(self, folder: Path, section: Union[str, Section] = None) -> None:
        self._configuration[Section.Root] = {section: {"__FOLDER__": folder}}
        if (folder / Global.CONFIG_FILE_NAME).exists():
            self._configuration[Section.Root][section].update(
                **read_json(str(folder / Global.CONFIG_FILE_NAME))
            )

    def _load_plugins_configs(self, plugins_folder: Path) -> None:
        for plugin_folder in plugins_folder.iterdir():
            # Read plugin's user configuration file
            user_folder: Path = Global.USER_ROOT / Global.CONFIGS_FOLDER / plugin_folder.name
            self._configuration[plugin_folder.name] = {
                Section.Inner: {"__FOLDER__": plugin_folder},
                Section.User: {"__FOLDER__": user_folder}
            }

            if (plugin_folder / Global.CONFIG_FILE_NAME).exists():
                # Read plugin's inner configuration file
                self._configuration[plugin_folder.name][Section.Inner].update({
                    **read_json(plugin_folder / Global.CONFIG_FILE_NAME),
                })

            if (plugin_folder / Global.CONFIG_FILE_NAME).exists():
                self._configuration[plugin_folder.name][Section.User].update({
                    **read_json(plugin_folder / Global.CONFIG_FILE_NAME),
                })

    def shutdown(self, *args, **kwargs) -> None:
        self._configuration = Dotty({})
        self._temp_configuration = Dotty({})

    def get(
        self,
        scope: Union[str, Section.Root] = Section.Root,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        key: Any = None,
        default: Any = None,
        temp: bool = False
    ) -> Any:
        """
        Get inner configuration value
        Args:
            scope (str|Section.Root): root/plugin configuration scope
            section (Section.Inner|Section.User): inner (plugin)/user configuration section
            key (str): configuration key
            default (Any): default value
            temp (bool): get the copied data
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        if temp and self._temp_configuration.get(f"{scope}.{section}"):
            return self._temp_configuration[f"{scope}.{section}.{key}"] or default

        return self._configuration.get(f"{scope}.{section}.{key}", default=default)

    def update(
        self,
        scope: Union[str, Section.Root] = Section.Root,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        key: Any = None,
        data: Any = None,
        temp: bool = False
    ) -> None:
        """
        Set data by section-key pair
        Args:
            scope (str|Section.Root): plugin/root configuration scope
            section (Section.Inner|Section.User): inner (plugin)/user configuration section
            key (str): configuration key
            data (Any): data to set
            temp (bool): create temporary configuration path with copied data
        """
        data_config_path = f"{scope}.{section}.{key}" if key else f"{scope}.{section}"
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        try:
            if temp:
                scope_config_path = f"{scope}.{section}"
                temp_copy = copy.deepcopy(self._configuration[scope_config_path])

                # Copy configuration into temporary configuration
                self._temp_configuration[scope_config_path] = temp_copy
                self._temp_configuration[scope_config_path].update(**temp_copy)
                self._temp_configuration[data_config_path] = data

            else:
                self._configuration[data_config_path] = data

        except KeyError as e:
            raise PieException(str(e))

    def delete(
        self,
        scope: Union[str, Section.Root] = Section.Root,
        section: Union[Section.Inner, Section.User] = Section.Inner,
        key: Any = None
    ) -> None:
        """
        Delete value by section-key pair
        Args:
            scope (str|Section.Root): plugin/root configuration scope
            section (Section.Inner|Section.User): inner (plugin)/user configuration section
            key (str): key to access data or nested data
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        try:
            del self._configuration[f"{scope}.{section}.{key}" if key else f"{scope}.{section}"]
        except KeyError as e:
            raise PieException(str(e))

    def restore(
        self,
        scope: Union[str, Section.Root],
        section: Union[Section.Inner, Section.User],
        key: Any = None
    ) -> None:
        """
        Restore configuration for given config path
        """
        self._logger.debug(f"Restoring {scope}.{section}")
        config_path = f"{scope}.{section}.{key}" if key else f"{scope}.{section}"

        if self._temp_configuration.get(f"{scope}.{section}"):
            self._temp_configuration[config_path] = self._configuration[config_path]

    def save(
        self,
        scope: Union[str, Section.Root],
        section: Union[Section.Inner, Section.User] = Section.Inner,
        temp: bool = False,
        create: bool = False
    ) -> None:
        """
        Save settings
        """
        # Check if temporary configuration exists
        scope_config_path = f"{scope}.{section}"

        if temp and self._temp_configuration.get(scope_config_path):
            configuration_data = copy.deepcopy(self._temp_configuration[scope_config_path])
        else:
            configuration_data = copy.deepcopy(self._configuration[scope_config_path])

        file_path: Path = configuration_data.get("__FOLDER__") / Global.CONFIG_FILE_NAME

        if not file_path.exists() and create:
            file_path.touch()

        self._configuration[scope_config_path] = configuration_data
        write_json(str(file_path), {k: v for (k, v) in configuration_data.items() if k != "__FOLDER__"})
