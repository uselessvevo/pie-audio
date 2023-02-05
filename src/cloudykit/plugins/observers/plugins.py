""" This observer serves """


class PluginObserverMixin:

    def __init__(self) -> None:
        self._plugin_availability_listeners = {}
        self._plugin_teardown_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, "_plugin_listen"):
                plugin_listen = method._plugin_listen

                # Check if plugin is listed among REQUIRES and OPTIONAL.
                # Note: We can"t do this validation for the Layout plugin
                # because it depends on all plugins through the Plugins.All
                # wildcard.
                if plugin_listen not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_listen}, but that plugin is not "
                        f"listed in REQUIRES nor OPTIONAL."
                    )

                # self._logger.debug(
                #     f"Method {method_name} is watching plugin {plugin_listen}"
                # )
                self._plugin_availability_listeners[plugin_listen] = method_name

            if hasattr(method, "_plugin_teardown"):
                plugin_teardown = method._plugin_teardown

                # Check if plugin is listed among REQUIRES and OPTIONAL.
                # Note: We can"t do this validation for the Layout plugin
                # because it depends on all plugins through the Plugins.All
                # wildcard.
                if plugin_teardown not in self.requires + self.optional:
                    raise Exception(
                        f"Method {method_name} of {self} is trying to watch "
                        f"plugin {plugin_teardown}, but that plugin is not "
                        f"listed in REQUIRES nor OPTIONAL."
                    )

                # self._logger.debug(f"Method {method_name} will handle plugin "
                #                   f"dispose for {plugin_teardown}")
                self._plugin_teardown_listeners[plugin_teardown] = method_name

    def on_plugin_available(self, plugin: str) -> None:
        if plugin in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners[plugin]
            method = getattr(self, method_name)
            # self._logger.debug(f"Calling {method}")
            method()

        # Call global plugin handler
        if "__all" in self._plugin_availability_listeners:
            method_name = self._plugin_availability_listeners["__all"]
            method = getattr(self, method_name)
            method(plugin)

    def on_plugin_teardown(self, plugin: str) -> None:
        pass
