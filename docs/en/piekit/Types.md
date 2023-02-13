# Types

## Expandable types
The following types are used in `ConfigLoader` to extend the default configuration. 

* EList - Expandable list
* EDict - Expandable dictionary

Usage example. Let's say, we have configuration files for system and application. In both files, we mark components list to expand application configuration by system configuration:

```py
# System
# system/config.py
COMPONENTS: EList = ["piekit.components.component.BuiltinComponent"]
```

```py
# Application
# %pieapp%/config.py
COMPONENTS: EList = ["pieapp.components.component.MyComponent"]
```

In result:
```py
>>> ["piekit.components.component.BuiltinComponent", "pieapp.components.component.MyComponent"]
```

> **Note**: It's important that the variables must be annotated by *expandable* types. Otherwhise they will be overwritten.

## Other data types

## **DirectoryType**

This type used to mark directories. For example, `AssetsManager` use it to ignore directories in `mount` method.
