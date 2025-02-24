from __feature__ import snake_case

import os
import sys

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication

from pieapp.api.globals import Global


class Application(QApplication):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.aboutToQuit.connect(self._cleanup_registries)

    def restart(self) -> None:
        if Global.IS_DEV_ENV is False:
            file_extension = "exe" if os.name == "nt" else ""
            sys.argv[0] = f"{sys.argv[0]}.{file_extension}"

        self._cleanup_registries()
        QProcess.start_detached(sys.executable, sys.argv)
        sys.exit()

    @staticmethod
    def _cleanup_registries() -> None:
        from pieapp.api.plugins.registry import PluginRegistry
        from pieapp.api.registries.registry import RegistryContainer

        PluginRegistry.shutdown_plugins(all_plugins=True)
        RegistryContainer.shutdown(all_registries=True)


def get_application(*args, **kwargs) -> Application:
    app = Application.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = Application(*args, **kwargs)

    return app
