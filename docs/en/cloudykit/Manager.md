# Managers

These classes used to solve single responsibility of services, configurations, resources, etc.
The base list of managers contains:

* `ConfigManager` - Configuration manager
* `LocalesManager` - Localization manager
* `AssetsManager` - Design resource manager
* `PluginsManager` - Plugin manager
* `ComponentsManager` - Component manager

All managers are inherited from `BaseManager`, which, like most objects in *cloudykit*, has basic methods: 

Initialization methods:

* `mount` - Initialize containers, variables and etc. To create object use `__init__` method
* `unmount` - Reset all containers, variables and etc. Don't use it to delete objects from memory

Methods for managing data in a container:

* `set` - Set data by key
* `get` - Get data by key
* `delete` - Delete data by key

Properties:
* `parent` - Parent object - `SystemManager`
* `registry` - Manager registry - `ManagerRegistry`
* `mounted` - Flag that indicates that object is mounted
