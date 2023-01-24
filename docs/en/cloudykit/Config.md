# Configuration

## Base directories
* `BASE_DIR <Path>` - root directory
* `APP_ROOT <Path>` - application root

## Plugins configuration
* `PLUGINS <EList>` - expandable list of plugins
* `PLUGINS_FOLDER <str>` - plugins directorty name
* `PLUGINS_USER_FOLDER <str>` - user plugins directorty name


## Components configuration
* `COMPONENTS_FOLDER <str>` - components directorty name
* `COMPONENTS <EList>` - expandable list of components


## Assets/resources configuration constants
* `ASSETS_EXCLUDED_FORMATS <EList>` - exnpandable list of excluded file formats
* `ASSETS_FOLDER <str>` - resources directory name (by default - "CLOUDYFF_ASSETS_FOLDER")
* `THEMES_FOLDER <str>` - themes directory name (by default - "CLOUDYFF_THEMES_FOLDER")


## Configuration
* `CONFIGS_FOLDER <str>` - configurations directory name
* `USER_CONFIGS_FOLDER <str>` - user configurations directory name
* `USER_FOLDER_FILES <EList>` - expandable list of user directory files; used for the first setup


## Localization configuration
* `DEFAULT_LOCALE <str>` - default language (by default - "en-US")
* `LOCALES_FOLDER <str>` - localization files directory name (by default - "locales")
* `LOCALES <EDict>` - expandable localization dictionary (locale code : language)


## Manager configuration
* `MANAGERS <EList>` - expandable list of `ManagerConfig`