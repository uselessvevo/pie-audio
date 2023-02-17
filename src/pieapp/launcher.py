import sys

from piekit.utils.core import except_hook
from pieapp.app.setup import setup_application
from pieapp.app.start import start_application


def launch():
    sys.excepthook = except_hook
    setup_application()
    start_application()


if __name__ == "__main__":
    launch()
