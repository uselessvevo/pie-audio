# Managers

These classes used to solve single responsibility of services, configurations, resources, etc.
The base list of managers contains:

* `ConfigManager` - configuration manager
* `LocalesManager` - localization manager
* `AssetsManager` - design resource manager
* `PluginsManager` - plugin manager
* `ComponentsManager` - component manager

All managers are inherited from `BaseManager`, which, like most objects in *cloudykit*, has basic methods: 

Initialization methods:

* `mount` - mounting the object
* `unmount` unmounting an object

Methods for managing data in a container:

* `set` - writing data to the container (for example, `dict`)
* `get` - getting data from the container 
* `delete` - deleting data

Attributes:
* `parent` - returns the parent object - `SystemManager`
* `registry` - returns the registry of objects - `ManagerRegistry`
* `mounted` - flag indicating that the object is mounted
