# Managers

These classes used to separate store and usage of the configurations and resources.
The built-in list of managers:

* `ConfigManager` - Configuration manager
* `LocalesManager` - Localization manager
* `AssetsManager` - Design resource manager
* `PluginsManager` - Plugin manager

All managers are inherited from `BaseManager`, which, like most objects in *piekit*, has basic methods: 

Initialization methods:

* `mount` - Initialize containers, variables and etc. To create object use `__init__` method
* `unmount` - Reset all containers, variables and etc. Don't use it to delete objects from memory

Methods for managing data in a container:

* `set` - Set data by key
* `get` - Get data by key
* `delete` - Delete data by key

Properties:
* `mounted` - Flag that indicates that object is mounted


# Manager Registry

To manage these classes, there is a special registry - `ManagersRegistry`,
that provides interfaces for managing managers. Such as:

* `mount` - mount managers
* `unmount` - unmount managers
* `reload` - reload managers
* `destroy` - delete managers

All methods above has special parameter - `managers` (list of managers) and `full_house` (get all mounted managers).

Unmount example:

```py
from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum

# First, unsafe method
Managers.unmount("configs")

# Second, safe method
Managers.unmount(SysManagersEnum.Configs)
```

Access example:

```py
from piekit.managers.registry import Managers
from piekit.structs.managers import SysManagersEnum

# First, unsafe method
Managers.configs.get(...)

# Second, safe method
Managers.get(SysManagersEnum.Configs).get(...)
```
