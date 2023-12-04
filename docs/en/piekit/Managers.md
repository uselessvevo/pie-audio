# Managers

> Attention: the principle of operation may change during the active development of the project

<br>

## Description
Managers are designed to manage resources separately under the principle of single-responsibility.

<br>

## Managers registration
To register managers, you need to write the import path to the manager with the class name in one of the categories or add it directly by calling the `from_string` or `from_class` method from the `ManagersRegistry` class.

<br>

## Registration via import line
```py
# globals.py
CORE_MANAGERS: Lock = [
    ...
    "piekit.managers.magic.MagicManagerClass",
    ...
]

# app.py
from piekit.managers.registry import Managers
from piekit.managers.magic.manager import MagicManagerClass

# Via import string
Managers.from_string("piekit.managers.magic.manager.MagicManager")

# Via manager class
Managers.from_class(MagicManagerClass)

# Calling manager's method
Managers("magic-manager").some_method(...)
```

<br>

# Manager's methods

## Method `init`
This optional method is designed to run the manager. For example, you can collect resources from plugins and put them into the manager's internal registry.

<br>

## Method `shutdown`
This optional method is intended to terminate the manager. For example, you can clear the manager's internal registry.

<br>

## Method `reload`
This optional method is used to restart the manager. By default, the `init` and `shutdown` methods are called.

<br>

## Method `__repr__`
This method outputs a string representation containing the name of the class and the `id` of its instance.
