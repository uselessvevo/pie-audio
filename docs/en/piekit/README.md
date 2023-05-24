## Application pre-configuraion
> *Notice*: At this moment, this application still in deep development and there is no reason to create installation package. First you need to download/clone the application:

1. Download via git - `git clone https://github.com/uselessvevo/cloudyff.git `
2. Install dependencies - `poetry init`.
> **Note**: If `poetry` is not installed - `pip install poetry`
4. Configure the environment variables:
* `PIE_CLOUDYAPP_ROOT` - application name
* `PIE_CONFIGS_FOLDER` - configuration directory; by default - config
* `PIE_USER_CONFIGS_FOLDER` - plugins directory; by default - os.path.expanduser("~")
* `PIE_PLUGINS_FOLDER` - plugins directory; by default - plugins
* `PIE_USER_PLUGINS_FOLDER` - directory of user plugins; by default - plugins
* `PIE_COMPONENTS_FOLDER` - directory of components; by default - components
* `PIE_ASSETS_FOLDER` - resource directory; default - assets
* `PIE_THEMES_FOLDER` - directory of themes; by default - themes

Now you need to set up the dev environment and run the file `pie-audio.py` or `pieapp/launcher.py `
