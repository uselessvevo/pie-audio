import sys

from piekit.managers.assets.utils import get_theme, get_palette
from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum
from piekit.utils.core import getApplication


def start_application():
    from pieapp.app.main import PieAudioApp
    qapp = getApplication()

    theme = Managers.get(SysManagersEnum.Assets).theme
    if theme:
        qapp.setStyleSheet(get_theme(theme))
        palette = get_palette(theme)
        if palette:
            qapp.setPalette(palette)

    pieApp = PieAudioApp()
    pieApp.prepare()
    pieApp.init()
    pieApp.show()

    sys.exit(qapp.exec_())
