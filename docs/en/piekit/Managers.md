## Managers

All managers are made for separated data storing and control (*single responsibility*).

To create your own manager you need next things:
* Create `BaseManager` or `PluginBaseManager` based class
* Define all the logic


```py
from piekit.managers.base import BaseManager


class MagicManager(BaseManager):
    name = "test-magic-manager"

    def __init__(self) -> None:
        self._logger = logger

    def init(self, *args, **kwargs) -> None:
        self._logger.debug("* Testing magic *")

    def shutdown(self, *args, **kwargs):
        self._logger.debug("No more magic...")

    def reload(self):
        self.shutdown()
        self.init()
```

After that you need to add it into managers registry (read `Manager Registry.md` file).
To get access to your registered manager (or other built-in managers) you need to do next:

* import `Managers` from `piekit.managers.registry`
* Managers(<manager name>).<manager method>(...)

Also, you can use mixins (read `Plugins.md`)