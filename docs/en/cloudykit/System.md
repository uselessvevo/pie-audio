# System manager


# Description
The main purpose of this manager is simplified access to managers and other services connected/mounted trough registries (for example, `ManagersRegistry). Additionally this manager solves the problem with recursive imports.

Contains:
* Registry of managers - `Managers Registry / registry`
* Configuration loader - `ConfigLoader / config`
* Information about the location of the application root directory - `APP_ROOT / root`
* Logging module (logger) - `logging.logger / logger`


# Usage Examples
Accessing the configuration

```py
>>> from cloudtykit.system.manager import System
>>> str(System.config.USER_CONFIGS_FOLDER / "directory name")
>>> "/path/to/cloudyff/directory/directory name"
```

Contacting the manager
```py
>>> from cloudtykit.system.manager import System
# # We get an instance of the `LocalesManager` class
>>> System.registry.locales("Username")
>>> "User Name"
```