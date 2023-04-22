import sys

from piekit.config import Config
from piekit.utils.core import getApplication
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers
from piekit.managers.assets.utils import getTheme, getPalette


def start_application():
    from pieapp.app.main import PieAudioApp
    qapp = getApplication()

    theme = Managers(SysManagers.Assets).getTheme()
    if theme:
        if Config.ASSETS_USE_STYLE:
            qapp.setStyleSheet(getTheme(theme))
            palette = getPalette(theme)
            if palette:
                qapp.setPalette(palette)

    pieApp = PieAudioApp()
    pieApp.prepare()
    pieApp.init()
    pieApp.show()

    sys.exit(qapp.exec())
