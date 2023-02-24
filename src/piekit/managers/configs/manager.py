import typing
from functools import lru_cache
from dotty_dict import Dotty

from piekit.managers.types import Sections, SysManagers
from piekit.managers.types import PathConfig
from piekit.managers.base import BaseManager
from piekit.system.exceptions import PieException
from piekit.utils.files import read_json, write_json
from piekit.observers.filesystem import FileSystemObserver


class ConfigManager(BaseManager):
    name = SysManagers.Configs
    protected_keys = ("__FILE__",)

    def __init__(self) -> None:
        super().__init__()

        self._roots: set[PathConfig] = set()
        self._configuration: Dotty[str, dict[str, typing.Any]] = Dotty({})
        self._observer = FileSystemObserver()

    def mount(self, *roots: PathConfig) -> None:
        for root_config in roots:
            self._roots.add(root_config)

            for file in root_config.root.rglob(root_config.pattern):
                section: str = root_config.root.name if root_config.section_stem else root_config.section

                if not self._configuration.get(section):
                    self._configuration[section] = {}

                if not self._configuration[section].get(file.name):
                    self._configuration[section][file.stem] = {}

                self._configuration[section]["__FILE__"] = file
                self._configuration[section][file.stem].update(**read_json(str(file)))

            self._observer.add_handler(str(root_config.root), str(root_config.root.name))

    def unmount(self, *args, **kwargs) -> None:
        self._configuration = Dotty({})
        self._observer.remove_handlers(full_house=True)

    def reload(self) -> None:
        self.unmount()
        self.mount(*self._roots)

    @lru_cache
    def get(
        self,
        section: typing.Union[str, Sections.Shared],
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
        section: typing.Union[str, Sections.Shared],
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
