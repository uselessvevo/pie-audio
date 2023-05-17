import typing
from functools import lru_cache
from pathlib import Path
from typing import Union, Any

from dotty_dict import Dotty

from piekit.config import Config
from piekit.config.exceptions import PieException
from piekit.managers.base import BaseManager
from piekit.managers.structs import Sections
from piekit.managers.structs import SysManagers
from piekit.utils.files import read_json, write_json
from piekit.observers.filesystem import FileSystemObserver
from piekit.utils.logger import logger


class ConfigManager(BaseManager):
    name = SysManagers.Configs
    protected_keys = ("__FILE__",)

    def __init__(self) -> None:
        self._logger = logger
        self._roots: set[Path] = set()
        self._configuration: Dotty[str, dict[str, Any]] = Dotty({})
        self._observer = FileSystemObserver()

    def init(self) -> None:
        # Read app/user configuration
        self._read_root_configuration(Config.APP_ROOT / Config.USER_CONFIG_FOLDER, Sections.Inner)
        self._read_root_configuration(Config.USER_ROOT / Config.USER_CONFIG_FOLDER, Sections.User)

        # Read plugin configuration
        self._read_plugins_configuration(Config.APP_ROOT / Config.CONTAINERS_FOLDER)
        self._read_plugins_configuration(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugins_configuration(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def _read_root_configuration(
        self,
        folder: Path,
        section: Union[str, Sections] = None
    ) -> None:
        self._roots.add(folder)
        self._configuration[Sections.Root] = {}

        for file in folder.rglob("*.json"):
            if not self._configuration[Sections.Root].get(section):
                self._configuration[Sections.Root][section] = {}

            if not self._configuration[Sections.Root][section].get(file.name):
                self._configuration[Sections.Root][section][file.stem] = {}

            self._configuration[Sections.Root][section]["__FILE__"] = file
            self._configuration[Sections.Root][section][file.stem].update(**read_json(str(file)))

        self._observer.add_handler(str(folder), str(folder.name))

    def _read_plugins_configuration(self, plugin_folder: Path) -> None:
        def read_config(section, package):
            for config in package.rglob("*.json"):
                if not self._configuration[section].get(config.name):
                    self._configuration[section][config.stem] = {}

                self._configuration[section]["__FILE__"] = config
                self._configuration[section][config.stem].update(**read_json(str(config)))

        for plugin_package in plugin_folder.iterdir():
            self._roots.add(plugin_package)

            # Plugin's inner configuration section - pieapp/plugins/<plugin name>/configs/
            inner_section = f"{plugin_package.name}.{Sections.Inner}"

            # Plugin's user configuration section - <user home folder>/configs/plugins/<plugin name>/
            user_section = f"{plugin_package.name}.{Sections.User}"
            user_folder: Path = Config.USER_ROOT / Config.CONFIGS_FOLDER / plugin_package.name

            if not self._configuration.get(inner_section):
                self._configuration[inner_section] = {}

            if not self._configuration.get(user_section):
                self._configuration[user_section] = {}

            # Read configuration from plugin's inner configuration folder
            read_config(inner_section, plugin_package)
            read_config(user_section, plugin_package)

            self._observer.add_handler(str(plugin_folder), str(plugin_folder.name))
            self._observer.add_handler(str(user_folder), str(user_folder.name))

    def shutdown(self, *args, **kwargs) -> None:
        self._configuration = Dotty({})
        self._observer.remove_handlers(full_house=True)

    @lru_cache
    def get(
        self,
        scope: Union[str, Sections] = Sections.Root,
        section: Union[str, Sections] = Sections.Inner,
        key: Any = None,
        default: Any = None,
    ) -> Any:
        """
        Get inner configuration value
        Args:
            scope (str|Sections): root/plugin configuration scope
            section (str): inner (plugin)/user configuration section
            key (Any): configuration key
            default (Any): default value
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        return self._configuration.get(f"{scope}.{section}.{key}", default)

    def get_shared(
        self,
        section: Union[Sections.Shared, Sections.User],
        key: str,
        default: Any = None,
    ) -> Any:
        return self.get(Sections.Root, section, key, default)

    def set(
        self,
        scope: Union[str, Sections] = Sections.Root,
        section: Union[str, Sections] = Sections.Inner,
        key: Any = None,
        data: Any = None
    ) -> None:
        """
        Set data by section-key pair
        Args:
            section (str|None): section name
            key (Any): key for the nested data
            data (Any): data to set
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        try:
            self._configuration[scope][section][key] = data
        except KeyError as e:
            raise PieException(str(e))

    def delete(
        self,
        scope: Union[str, Sections] = Sections.Root,
        section: Union[str, Sections] = Sections.Inner,
        key: Any = None
    ) -> None:
        """
        Delete value by section-key pair
        Args:
            section (str|None): section name
            key (Any): key to access data or nested data
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        try:
            if not key:
                del self._configuration[scope][section]
            else:
                del self._configuration[scope][section][key]

        except KeyError as e:
            raise PieException(str(e))

    def save(
        self,
        scope: Union[str, Sections] = Sections.Root,
        section: Union[str, Sections] = Sections.Inner,
        data: dict = None,
        create: bool = False
    ) -> None:
        """
        Save user settings
        """
        try:
            file = self._configuration[scope][section]["__FILE__"]
            folder = file.parent
        except KeyError as e:
            raise PieException(str(e))

        if create:
            try:
                if not folder.exists():
                    folder.mkdir()
                self._configuration[scope].update({section: data})
            except (OSError, KeyError) as e:
                raise PieException(str(e))

        write_json(str(file), data)
        self._configuration[scope][section] = data
