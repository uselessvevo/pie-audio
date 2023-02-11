import typing
from dotty_dict import Dotty
from functools import lru_cache

from piekit.structs.etc import SharedSection
from piekit.structs.configs import PathConfig
from piekit.managers.base import BaseManager
from piekit.utils.files import read_json, write_json
from piekit.observers.filesystem import FileSystemObserver


class ConfigManager(BaseManager):
    name = "configs"
    protected_keys = ("__FILE__",)

    def __init__(self) -> None:
        super().__init__()

        self._roots: set[PathConfig] = set()
        self._dictionary: Dotty = Dotty({})
        self._observer = FileSystemObserver()

    def mount(self, *roots: PathConfig) -> None:
        for root_config in roots:
            self._roots.add(root_config)

            for file in root_config.root.rglob(root_config.pattern):
                section: str = root_config.root.name if root_config.section_stem else root_config.section

                if not self._dictionary.get(section):
                    self._dictionary[section] = {}

                if not self._dictionary[section].get(file.name):
                    self._dictionary[section][file.stem] = {}

                self._dictionary[section]["__FILE__"] = file
                self._dictionary[section][file.stem].update(**read_json(str(file)))

            self._observer.add_handler(str(root_config.root), str(root_config.root.name))

    def unmount(self, *args, **kwargs) -> None:
        self._dictionary = Dotty({})
        self._observer.remove_handlers(full_house=True)

    def reload(self) -> None:
        self.unmount()
        self.mount(*self._roots)

    @lru_cache
    def get(
        self,
        section: typing.Union[str, SharedSection],
        key: typing.Any = None,
        default: typing.Any = None
    ) -> typing.Any:
        """
        Get value by section-key pair

        Args:
            section (str|None): section name
            key (Any): key to access data or nested data
            default (Any): default value if key was not found
        """
        if key in self.protected_keys:
            raise KeyError(f"Can't use protected key: {key}")

        return self._dictionary.get(f"{section}.{key}", default)

    def set(
        self,
        section: str,
        key: typing.Any = None,
        data: typing.Any = None
    ) -> None:
        """
        Set data by section-key pair

        Args:
            section (str|None): section name
            key (Any): key to access nested data
            data (Any): data to set
        """
        if key in self.protected_keys:
            raise KeyError(f"Can't use protected key: {key}")

        self._dictionary[section][key] = data

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
            raise KeyError(f"Can't use protected key: {key}")

        if not key:
            del self._dictionary[section]
        else:
            del self._dictionary[section][key]

    def save(self, section: str, data: dict, create: bool = False) -> None:
        try:
            file = self._dictionary[section]["__FILE__"]
            folder = file.parent
        except KeyError:
            raise FileNotFoundError(f"Folder `{section}` doesn't exist")

        if create:
            if not folder.exists():
                folder.mkdir()
            self._dictionary.update({section: data})

        if not self._dictionary.get(section):
            raise FileNotFoundError(f"File {section} not found")

        write_json(str(file), data)
        self._dictionary[section] = data
