import os
from typing import Tuple


def _get_screen_info_unix() -> Tuple[int, int]:
    import subprocess
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',
                              shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return resolution[0], resolution[1]


def _get_screen_info_windows() -> Tuple[int, int]:
    import ctypes
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_screen_info() -> Tuple[int, int]:
    if os.name in 'windows':
        return _get_screen_info_windows()

    elif os.name in ('posix', 'darwin'):
        return _get_screen_info_unix()

    else:
        raise RuntimeError('unknown platform (can\'t get resolution)')


getScreenInfo = get_screen_info
