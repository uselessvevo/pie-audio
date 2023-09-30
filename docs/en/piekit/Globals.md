# Application global fields

# Magic/special annotations

Magic handlers are made to control fields and their data in the globals module. To add them in the `GlobalLoader` you need to use `add_handler` method:

```py
from piekit.globals import Global, Lock, Min, Max

Config.add_handlers(Lock, Min, Max)
```

For example, we have the magic annotation - `Lock` that can protect it from value change.
How to do that? It's very simple: `TEST_STRING_FIELD: Lock = "Test String Field"`.
After that you will not be able change it's value - handler will trhrow warning.

Besides a `Lock`, piekit has `Max` and `Min` magic annotations that allows you to set max and min field value.
For example:

```py
from piekit.globals.types import Min, Max

TEST_MIN_FIELD: Min[3] = [1, 2]
TEST_MAX_FIELD: Max[3] = [1, 2, 3, 4]
```

When declaring both fields, a warning about the impossibility of setting these values will be displayed.


# Default fields (piekit.pieaudio-ver)

# Directories
* `BASE_DIR <pathlib.Path>` - root directory (by default - "PIE_BASE_DIR")
* `APP_ROOT <pathlib.Path>` - application directory (by default - "PIE_APP_ROOT")
* `USER_ROOT <pathlib.Path>` - user root directory (by default - "PIE_USER_ROOT")
* `SYSTEM_ROOT <pathlib.Path>` - piekit root directory (by default - "piekit")

# Plugins
* `PLUGINS_FOLDER <str>` - plugins folder name (by default - "PIE_PLUGINS_FOLDER")
* `CONTAINERS_FOLDER <str>` - containers folder name (by default - "PIE_CONTAINERS_FOLDER")

# Resources/assets
* `ASSETS_FOLDER <str>` - assets folder name (by default - "PIE_ASSETS_FOLDER" or "assets")
* `THEMES_FOLDER <str>` - themes folder name (by default - "PIE_THEMES_FOLDER" or "themes")
* `DEFAULT_THEME <str>` - theme by default (selects among the available themes in the `ASSETS_FOLDER`)
* `ASSETS_USE_STYLE <str>` - use stylesheet or not (by default - "PIE_ASSETS_USE_STYLE" or True)
* `ASSETS_EXCLUDED_FORMATS <list>` - list of the excluded file formats (by default - empty list)

# Configuration folders
* `CONFIGS_FOLDER <str>` - configuration folder name (by default - "PIE_CONFIGS_FOLDER" or "configs")
* `USER_CONFIGS_FOLDER <str>` - user configuration folder name (by default - "PIE_USER_CONFIGS_FOLDER" or "configs")

# Language/Localization
* `DEFAULT_LOCALE <str>` - language by default (by default - "PIE_DEFAULT_LOCALE" or "en-US")
* `LOCALES_FOLDER <str>` - localization folder name (by default - "PIE_LOCALES_FOLDER" or "locales")
* `LOCALES <dict>` - locales dictionary

# Managers
* `MANAGERS <list>` - managers list


# ConfigLoader

Global loader is used to load extensible global fields from python modules. by default, the module specified in the environment variables is loaded (by default - `piekit.globals.globals`).

To load the globals module of your application, you need to add it yourself using the `load_module` method.

Setup example:

```py
Config.import_module(os.getenv("PIE_SYS_GLOBALS_MODULE", "pekit.globals.globals"))
```
