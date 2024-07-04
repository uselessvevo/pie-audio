import functools


def on_plugin_available(func: callable = None, plugin: str = None) -> callable:
    if func is None:
        return functools.partial(on_plugin_available, plugin=plugin)

    func.plugin_listen = plugin
    return func


def on_plugin_shutdown(func: callable = None, plugin: str = None) -> callable:
    if func is None:
        return functools.partial(on_plugin_shutdown, plugin=plugin)

    func.plugin_teardown = plugin
    return func
