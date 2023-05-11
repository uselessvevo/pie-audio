from __feature__ import snake_case

import sys

from piekit.config import Config
from piekit.utils.core import get_application
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManagers
from piekit.managers.assets.utils import get_theme, get_palette


def start_application():
    from pieapp.app.main import PieAudioApp
    qapp = get_application()

    theme = Managers(SysManagers.Assets).get_theme()
    if theme:
        if Config.ASSETS_USE_STYLE:
            qapp.set_style_sheet(get_theme(theme))
            palette = get_palette(theme)
            if palette:
                qapp.set_palette(palette)

    pieApp = PieAudioApp()
    pieApp.prepare()
    pieApp.init()
    pieApp.show()

    sys.exit(qapp.exec())
