import typing
from functools import lru_cache
from pathlib import Path
from typing import Union

from dotty_dict import Dotty

from piekit.managers.structs import Sections, SysManagers
from piekit.managers.base import BaseManager
from piekit.config.exceptions import PieException
from piekit.config import Config
from piekit.utils.files import read_json, write_json
from piekit.observers.filesystem import FileSystemObserver


class ConfigManager(BaseManager):
    name = SysManagers.Configs
    protected_keys = ("__FILE__",)

    def __init__(self) -> None:
        super().__init__()

        self._roots: set[Path] = set()
        self._configuration: Dotty[str, dict[str, typing.Any]] = Dotty({})
        self._observer = FileSystemObserver()

    def mount(self) -> None:
        # Read app/user configuration
        self._read_root_configuration(Config.APP_ROOT / Config.USER_CONFIG_FOLDER, Sections.Shared)
        self._read_root_configuration(Config.USER_ROOT / Config.USER_CONFIG_FOLDER, Sections.User)

        # Read plugin configuration
        self._read_plugin_configuration(Config.APP_ROOT / Config.PLUGINS_FOLDER)
        self._read_plugin_configuration(Config.USER_ROOT / Config.USER_PLUGINS_FOLDER)

    def _read_root_configuration(self, folder: Path, section: Union[str, Sections] = None) -> None:
        self._roots.add(folder)

        for file in folder.rglob("*.json"):
            section = section if section else file.parent.name
            if not self._configuration.get(section):
                self._configuration[section] = {}

            if not self._configuration[section].get(file.name):
                self._configuration[section][file.stem] = {}

            self._configuration[section]["__FILE__"] = file
            self._configuration[section][file.stem].update(**read_json(str(file)))

        self._observer.add_handler(str(folder), str(folder.name))

    def _read_plugin_configuration(self, folder: Path) -> None:
        for package in folder.iterdir():
            self._roots.add(package)

            for file in package.rglob("*.json"):
                section = package.name
                if not self._configuration.get(section):
                    self._configuration[section] = {}

                if not self._configuration[section].get(file.name):
                    self._configuration[section][file.stem] = {}

                self._configuration[section]["__FILE__"] = file
                self._configuration[section][file.stem].update(**read_json(str(file)))

            self._observer.add_handler(str(folder), str(folder.name))

    def unmount(self, *args, **kwargs) -> None:
        self._configuration = Dotty({})
        self._observer.remove_handlers(full_house=True)

    def reload(self) -> None:
        self.unmount()
        self.mount()

    @lru_cache
    def get(
        self,
        section: typing.Union[str, Sections],
        key: typing.Any = None,
        default: typing.Any = None
    ) -> typing.Any:
        """
        Get value by section-key pair

        Args:
            section (str|None): section name
            key (Any): key for the nested data
            default (Any): default value if key was not found
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        return self._configuration.get(f"{section}.{key}", default)

    def set(
        self,
        section: typing.Union[str, Sections],
        key: typing.Any = None,
        data: typing.Any = None
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

        self._configuration[section][key] = data

    def delete(
        self,
        section: str,
        key: typing.Any = None
    ) -> None:
        """
        Delete value by section-key pair

        Args:
            section (str|None): section name
            key (Any): key to access data or nested data
        """
        if key in self.protected_keys:
            raise PieException(f"Can't use protected key: {key}")

        if not key:
            del self._configuration[section]
        else:
            del self._configuration[section][key]

    def save(self, section: str, data: dict, create: bool = False) -> None:
        try:
            file = self._configuration[section]["__FILE__"]
            folder = file.parent
        except KeyError:
            raise PieException(f"Folder `{section}` doesn't exist")

        if create:
            if not folder.exists():
                folder.mkdir()
            self._configuration.update({section: data})

        if not self._configuration.get(section):
            raise PieException(f"File {section} not found")

        write_json(str(file), data)
        self._configuration[section] = data
