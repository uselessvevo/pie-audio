from __feature__ import snake_case

import sys

from piekit.config import Config
from piekit.utils.core import get_application
from piekit.managers.registry import Managers
from piekit.managers.structs import SysManager
from piekit.managers.assets.utils import get_theme, get_palette


def start_application():
    from pieapp.app.main import PieAudioApp
    app = get_application()

    theme = Managers(SysManager.Assets).get_theme()
    if theme:
        if Config.ASSETS_USE_STYLE:
            app.set_style_sheet(get_theme(theme))
            palette = get_palette(theme)
            if palette:
                app.set_palette(palette)

    pie_app = PieAudioApp()
    pie_app.prepare()
    pie_app.init()
    pie_app.show()

    sys.exit(app.exec())
