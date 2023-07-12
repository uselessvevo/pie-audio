import copy
from pathlib import Path
from typing import Union, Any

from dotty_dict import Dotty

from piekit.config import Config
from piekit.config.exceptions import PieException
from piekit.managers.base import BaseManager
from piekit.managers.structs import Section
from piekit.managers.structs import SysManager
from piekit.utils.files import read_json, write_json
from piekit.observers.filesystem import FileSystemObserver
from piekit.utils.logger import logger


class ConfigManager(BaseManager):
    name = SysManager.Configs
    protected_keys = ("__FILES__",)

    def __init__(self) -> None:
        self._logger = logger
        self._configuration: Dotty[str, dict[str, Any]] = Dotty({})
        self._temp_configuration: Dotty[str, dict[str, Any]] = Dotty({})
        self._observer = FileSystemObserver()

    def init(self) -> None:
        # Read app/user configuration
        self._read_root_configuration(Config.APP_ROOT / Config.USER_CONFIG_FOLDER, Section.Inner)
        self._read_root_configuration(Config.USER_ROOT / Config.USER_CONFIG_FOLDER, Section.User)

        # Read plugin configuration
        self._read_plugins_configuration(Config.APP_ROOT / Config.CONTAINERS_FOLDER)
        self._read_plugins_configuration(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugins_configuration(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def _read_root_configuration(
        self,
        folder: Path,
        section: Union[str, Section] = None
    ) -> None:
        self._configuration[Section.Root] = {}
        self._configuration[Section.Root]["__FILES__"] = list(i for i in folder.rglob("configs/*.json"))

        for file in folder.rglob("*.json"):
            if not self._configuration[Section.Root].get(section):
                self._configuration[Section.Root][section] = {}

            if not self._configuration[Section.Root][section].get(file.name):
                self._configuration[Section.Root][section][file.stem] = {}

            self._configuration[Section.Root][section][file.stem].update(**read_json(str(file)))

        self._observer.add_handler(str(folder), str(folder.name))

    def _read_plugins_configuration(self, plugins_folder: Path) -> None:
        def read_config(section, package):
            self._configuration[section]["__FILES__"] = list(i for i in package.rglob("configs/*.json"))

            for config in package.rglob("configs/*.json"):
                if not self._configuration[section].get(config.name):
                    self._configuration[section][config.stem] = {}

                self._configuration[section][config.stem].update(**read_json(str(config)))

        for plugin_folder in plugins_folder.iterdir():
            # Plugin's inner configuration section - pieapp/plugins/<plugin name>/configs/
            inner_section = f"{plugin_folder.name}.{Section.Inner}"

            # Plugin's user configuration section - <user home folder>/configs/plugins/<plugin name>/
            user_section = f"{plugin_folder.name}.{Section.User}"
            user_folder: Path = Config.USER_ROOT / Config.CONFIGS_FOLDER / plugin_folder.name

            if not self._configuration.get(inner_section):
                self._configuration[inner_section] = {}

            if not self._configuration.get(user_section):
                self._configuration[user_section] = {}

            # Read configuration from plugin's inner configuration folder
            read_config(inner_section, plugin_folder)
            read_config(user_section, user_folder)

            self._observer.add_handler(str(plugins_folder), str(plugins_folder.name))
            self._observer.add_handler(str(user_folder), str(user_folder.name))

    def shutdown(self, *args, **kwargs) -> None:
        self._configuration = Dotty({})
        self._observer.remove_handlers(full_house=True)

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

        return self._configuration.get(f"{scope}.{section}.{key}") or default

    def set(
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
                if not self._temp_configuration.get(scope_config_path):
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

    def copy(
        self,
        target_from: dict,
        target_into: dict,
    ) -> None:
        pass

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

        if self._temp_configuration[f"{scope}.{section}"]:
            self._temp_configuration[config_path] = self._configuration[config_path]

    def save(
        self,
        scope: Union[str, Section.Root],
        section: Union[Section.Inner, Section.User] = Section.Inner,
        file_section: Union[str, None] = None,
        temp: bool = False
    ) -> None:
        """
        Save settings
        """
        # Check if temporary configuration exists
        scope_config_path = f"{scope}.{section}"

        if temp and self._temp_configuration.get(scope_config_path):
            configuration_data = self._temp_configuration[scope_config_path]
        else:
            configuration_data = self._configuration[scope_config_path]

        if file_section:
            files: list[Path] = self._configuration[f"{scope}.{section}.{file_section}"]
        else:
            files: list[Path] = self._configuration[f"{scope}.{section}"]["__FILES__"]

        del configuration_data["__FILES__"]

        files_zip = dict(zip(configuration_data.keys(), files))

        for file_scope, file_path in files_zip.items():
            write_json(str(file_path), configuration_data.get(file_scope))
