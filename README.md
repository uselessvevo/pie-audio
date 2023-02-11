## Pie Audio - An experimental audio/video converter
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

[English docs](https://github.com/uselessvevo/pieaudio/tree/docs/docs/en/piekit) • [Русский docs](https://github.com/uselessvevo/pieaudio/tree/docs/docs/ru/cloudykit)

## Application pre-configuration
> *Notice*: At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/pieaudio.git `
2. Create virtual environment
3. Install dependencies - `pip install -r requirements/<your platform>.txt`.
4. Configure the environment variables:
* `PIEAPP_ENTRYPOINT` - application name
* `CONFIGS_FOLDER` - configuration directory; by default - config
* `USER_CONFIGS_FOLDER` - plugins directory; by default - os.path.expanduser("~")
* `PLUGINS_FOLDER` - plugins directory; by default - plugins
* `USER_PLUGINS_FOLDER` - directory of user plugins; by default - plugins
* `COMPONENTS_FOLDER` - directory of components; by default - components
* `ASSETS_FOLDER` - resource directory; default - assets
* `THEMES_FOLDER` - directory of themes; by default - themes

Now you need to set up the dev environment and run the file `pieapp/launcher.py `
