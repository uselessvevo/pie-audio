# Global settings

> Attention: the principle of operation may change during the active development of the project

<br>


## Description
This module is designed to access the global settings of the application with the ability to use handlers through field annotations.

<br>

## Special field annotations
These micropro-handlers are used to control fields and their values via [type annotations](https://peps.python.org/pep-0484/). For more details, read the documentation [confstar documentation](https://github.com/uselessvevo/confstar).

<br>

## Location of Global configuration modules
In addition to the global configuration system module, that located in `piekit/globals`, you can also create your own by placing them in `pieapp/app` or in the root directory of the plugin. 

After that you need to prepare `ConfLoader` and load configuration modules:

```py
# piekit/globals/loader.py
from confstar import ConfLoader

Global = ConfLoader()

# pieapp/start.py
from confstar.types import Lock, Min, Max
from piekit.globals import Global

Global.add_handlers(Lock, Min, Max)
# or via `Global.load_by_path()`
Global.import_module("piekit.globals.globals") 
Global.import_module("pieapp.app.globals")
```

<br>

# The main fields of the application

## PIEAPP_APPLICATION_NAME 
Return value: `<Lock[str]>`

Name of the application

<br>

## PIEAPP_APPLICATION_VERSION
Return value: `<Lock[str]>`

Application Version


<br>

## PIEAPP_ORGANIZATION_NAME 
Return value: `<Lock[str]>`

Name of the organization

<br>

## PIEAPP_ORGANIZATION_DOMAIN
Return value: `<Lock[str]>`

The organization's domain

<br>

## PIEAPP_PROJECT_URL  
Return value: `<Lock[str]>`

Link to the project

<br>

# System fields

## PIEKIT_VERSION 
Return value: `<Lock[str]>`

The `piekit` version

<br>

## BASE_DIR
Return value: `<Lock[pathlib.Path]>`

The root directory

<br>

## APP_ROOT
Return value: `<Lock[pathlib.Path]>`

The root directory of the application (`pieapp`)

<br>

## SYSTEM_ROOT
Return value: `<Lock[pathlib.Path]>`

The root directory of the system (`piekit')

<br>

## USER_ROOT
Return value: `<Lock[pathlib.Path]>`

The user's root directory (`/home/user/` or `C:\Users\User `)

<br>

## DEFAULT_TEMP_FOLDER_NAME
Return value: `<Lock[str]>`

The name of the temporary files directory by default

<br>

# Directories, files and resource fields 

## PLUGINS_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the plugin directory

<br>

## CONF_PAGES_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the module directory of the settings pages

<br>

## DEFAULT_PLUGIN_ICON_NAME
Return value: `<Lock[str]>`

Name of the plugin icon

<br>

# Directories, files and resource fields

## ASSETS_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the resource directory

<br>

## THEMES_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the resource directory

<br>

## ICONS_ALLOWED_FORMATS
Return value: <list[str]>

List of allowed icon formats

<br>

## DEFAULT_THEME_NAME
Return value: `<Lock[str]>`

Default theme name

<br>

## THEME_USE_STYLESHEET
Return value: `<Lock[bool]>`

Whether to use cascading style sheets. By default, `True`

<br>

# Directories, files and resource fields 

## CONFIGS_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the configuration directory

<br>

## CONFIG_FILE_NAME
Return value: `<Lock[str]>`

Name of the configuration file

<br>

# Directories, files and resource fields 

## LOCALES_FOLDER_NAME
Return value: `<Lock[str]>`

Name of the translation file directory

<br>


## DEFAULT_LOCALE_NAME
Return value: `<Lock[str]>`

Default locale name

<br>

## LOCALES_DICT
Return value: <dict[str, str]>

Dictionary with available localizations