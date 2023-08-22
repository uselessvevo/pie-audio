"""
Base manager
"""
from pathlib import Path


class BaseManager:
    # Manager name
    name: str

    def init(self, *args, **kwargs) -> None:
        """
        Optional initializer
        """

    def shutdown(self, *args, **kwargs):
        """
        This method serves to reset all containers, variables etc.
        Don't use it to delete data from memory
        """

    def reload(self):
        """
        This method reload manager
        """
        self.shutdown()
        self.init()

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f'({self.__class__.__name__}) <id: {id(self)}>'


class PluginManager(BaseManager):

    def init_plugin(self, plugin_folder: Path) -> None:
        raise NotImplementedError(f"Method `init_plugin` must be implemented")

    def on_post_init_plugin(self, plugin_folder: Path) -> None:
        pass

    def shutdown_plugin(self) -> None:
        raise NotImplementedError(f"Method `shutdown_plugin` must be implemented")

    def on_post_shutdown(self) -> None:
        pass
