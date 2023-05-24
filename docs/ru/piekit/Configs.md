# Настройка конфигурации приложения

# Специальные аннотации полей

Данные обработчики используются для контроля полей и их значений. Для добавления обработчиков используется метод `add_handler`:

```py
from piekit.config import Config, Lock, Min, Max

Config.add_handlers(Lock, Min, Max)
```

К примеру, у нас имеется аннотация - `Lock`, которая позволяет заблокировать изменение значения поля.
Как это сделать? Всё очень просто: `TEST_STRING_FIELD: Lock = "Test String Field"`
При попытке изменить значение будет выведено предупреждение о невозможности изменения значения поля.

Помимо `Lock` в piekit имеется: `Max` и `Min`, позволяющие установить максимальное и минимальное значение поля. 
К примеру:
```py
from piekit.config.types import Min, Max

TEST_MIN_FIELD: Min[3] = [1, 2]
TEST_MAX_FIELD: Max[3] = [1, 2, 3, 4]
```

При объявлении обоих полей будет выведено предупреждение о невозможности установления данных значений.


# Поля по-умолчанию (piekit.pieaudio-ver)

# Директории
* `BASE_DIR <pathlib.Path>` - корневая директория (по-умолчанию - "PIE_BASE_DIR")
* `APP_ROOT <pathlib.Path>` - директория приложения (по-умолчанию - "PIE_APP_ROOT")
* `USER_ROOT <pathlib.Path>` - директория пользователя (по-умолчанию - "PIE_USER_ROOT")
* `SYSTEM_ROOT <pathlib.Path>` - директория piekit (по-умолчанию - "piekit")

# Настройки плагинов
* `PLUGINS_FOLDER <str>` - наименование директории плагинов (по-умолчанию - "PIE_PLUGINS_FOLDER")
* `CONTAINERS_FOLDER <str>` - наименование директории контейнеров (по-умолчанию - "PIE_CONTAINERS_FOLDER")

# Настройки ресурсов
* `ASSETS_FOLDER <str>` - наименование директории ресурсов (по-умолчанию - "PIE_ASSETS_FOLDER" или "assets")
* `THEMES_FOLDER <str>` - наименование директории ресурсов (по-умолчанию - "PIE_THEMES_FOLDER" или "themes")
* `DEFAULT_THEME <str>` - тема по-умолчанию; выбирает среди доступных тем в директории `ASSETS_FOLDER`
* `ASSETS_USE_STYLE <str>` - использовать ли тему оформления (по-умолчанию - "PIE_ASSETS_USE_STYLE" или True)
* `ASSETS_EXCLUDED_FORMATS <list>` - список исключённых форматов файлов (по-умолчанию - пустой список)

# Настройка директорий конфигураций
* `CONFIGS_FOLDER <str>` - наименование директории конфигураций (по-умолчанию - "PIE_CONFIGS_FOLDER" или "configs")
* `USER_CONFIGS_FOLDER <str>` - наименование директории пользовательских конфигураций (по-умолчанию - "PIE_USER_CONFIGS_FOLDER" или "configs")

# Настройки локализации
* `DEFAULT_LOCALE <str>` - язык по-умолчанию (по-умолчанию - "PIE_DEFAULT_LOCALE" или "en-US")
* `LOCALES_FOLDER <str>` - наименование директории файлов переводов (по-умолчанию - "PIE_LOCALES_FOLDER" или "locales")
* `LOCALES <dict>` - словарь с локализациями

# Настройка менеджеров
* `MANAGERS <list>` - список словарей с конфигурацией запуска менеджеров


# ConfigLoader

ConfigLoader используется для загрузки конфигураций с возможностью расширения из python-модулей. По-умолчанию загружается модуль, указанный в переменных окружения (по-умолчанию - `piekit.system.config`).

Для загрузки модуля конфигураций вашего приложения его нужно добавить самостоятельно, используя метод `load_module`.

Пример настройки:

```py
Config.import_module(os.getenv("CONFIG_MODULE_NAME", "pekit.config.config"))
```
