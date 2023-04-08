## Pie Audio - Lightweight audio converter with plugins support

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

[English docs](https://github.com/uselessvevo/pie-audio/tree/docs/docs/en/piekit) • [Русский docs](https://github.com/uselessvevo/pie-audio/tree/docs/docs/ru/piekit)

## Special thanks
I want to say thanks to spyder-ide - part of the code is based on this project.

## Before the start
> *Notice*: At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/pie-audio.git `
2. Install poetry - `pip install poetry`
3. Initialize poetry - `poetry init`
4. Configure the environment variables (optional):
* `CONFIGS_FOLDER` - configuration directory; by default - config
* `USER_CONFIGS_FOLDER` - plugins directory; by default - os.path.expanduser("~")
* `PLUGINS_FOLDER` - plugins directory; by default - plugins
* `USER_PLUGINS_FOLDER` - directory of user plugins; by default - plugins
* `COMPONENTS_FOLDER` - directory of components; by default - components
* `ASSETS_FOLDER` - resource directory; default - assets
* `THEMES_FOLDER` - directory of themes; by default - themes
5. Run program - `poetry shell` and `python ./pie-audio.py'
