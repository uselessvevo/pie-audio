## CloudyFF - An experimental audio/video converter
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

[English readme](https://github.com/uselessvevo/cloudyff/tree/docs/docs/en/cloudykit) • [Русский readme](https://github.com/uselessvevo/cloudyff/tree/docs/docs/ru/cloudykit)

## Application pre-configuraion
> *Notice*: At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/cloudyff.git `
2. Install dependencies - `poetry init`.
> **Note**: If `poetry` is not installed - `pip install poetry`
4. Configure the environment variables:
* `CLOUDYAPP_ROOT` - application name
* `CONFIGS_FOLDER` - configuration directory; by default - config
* `USER_CONFIGS_FOLDER` - plugins directory; by default - os.path.expanduser("~")
* `PLUGINS_FOLDER` - plugins directory; by default - plugins
* `USER_PLUGINS_FOLDER` - directory of user plugins; by default - plugins
* `COMPONENTS_FOLDER` - directory of components; by default - components
* `ASSETS_FOLDER` - resource directory; default - assets
* `THEMES_FOLDER` - directory of themes; by default - themes

Now you need to set up the dev environment and run the file `cloudyapp/launcher.py `
