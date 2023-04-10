# Application pre-configuraion

At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/pie-audio`
2. Install dependencies - `poetry init`.
> **Note**: If `poetry` is not installed - `pip install poetry`
4. Configure the environment variables:
* `PIEAPP_ROOT` - application name
* `CONFIGS_FOLDER` - configuration directory; by default - config
* `USER_CONFIGS_FOLDER` - plugins directory; by default - os.path.expanduser("~")
* `PLUGINS_FOLDER` - plugins directory; by default - plugins
* `USER_PLUGINS_FOLDER` - directory of user plugins; by default - plugins
* `COMPONENTS_FOLDER` - directory of components; by default - components
* `ASSETS_FOLDER` - resource directory; default - assets
* `THEMES_FOLDER` - directory of themes; by default - themes

Now you need to set up the dev environment and run the file `pie-audio.py `
