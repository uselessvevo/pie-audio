## Manager registry

To manage manager classes we have a special registry `ManagersRegistry`. It provides methods for managing managers. Such as:

## Method `from_class`
Description:
    Initializes manager from its type

Arguments:
    manager_class (ModuleType[BaseManager|PluginBaseManager]): manager class
    init (bool): call `init` method to initialize manager
    args (tuple[Any]): tuple of additional positionl arguments
    kwargs (dict[Any, Any]): tuple of additional keyword arguments

Returns:
    NoneType


## Method `from_config`
Description:
    Initializes manager from `ManagerConfig` model

Arguments:
    config (ManagerConfig): manager configuration model

Returns:
    NoneType


## Method `from_json`
Description:
    Initializes manager from json file

Arguments:
    file (str, pathlib.Path): configuration json file

Returns:
    NoneType


## Method `shutdown`
Description:
    Shutdown given `managers` by calling `shutdown` method. Or you can pass `full_house` to get all managers.

Arguments:
    managers (list[str]): list of managers name
    full_house (bool): get all managers

Returns:
    NoneType


## Method `reload`
Description:
    Reload given `managers` by calling `reload` method. Or you can pass `full_house` to get all managers.

Arguments:
    managers (list[str]): list of managers name
    full_house (bool): get all managers

Returns:
    NoneType


## Method `destroy`
Description:
    Destroy given `managers` by calling `destroy` method. Or you can pass `full_house` to get all managers.

Arguments:
    managers (list[str]): list of managers name
    full_house (bool): get all managers

Returns:
    NoneType


## Method `get_plugin_managers`
Description:
    Get all managers that can setup plugins.

Returns:
    List of `PluginBaseManager` (list[PluginBaseManager])


## Method `__call__`
Description:
    Get manager instance

Arguments:
    manager (str): manager name
    fallback_method (callable): method to call if manager was not found

Returns:
    Manager instance (BaseManager|PluginBaseManager)
