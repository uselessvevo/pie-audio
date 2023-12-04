# Глобальные настройки

> Внимание: принцип работы может менятся в течении активной разработки проекта

<br>

## Описание
Данный модуль предназначен для доступа к глобальным настройкам приложения с возможностью использования обработчиков через аннотации полей.

<br>

## Специальные аннотации полей
Данные микрообработчики используются для контроля полей и их значений [через аннотации типов](https://peps.python.org/pep-0484/). За подробностями, читайте документацию к [confstar](https://github.com/uselessvevo/confstar).

После этого вам требуется подготовить `ConfLoader` и загрузить конфигурационные модули:

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

## Расположение модулей глобальных настроек
Помимо системного модуля глобальных настроек, находящиеся в `piekit/globals`, вы так же можете создать свои, расположив в `pieapp/app` или в корне директории плагина.

<br>

# Основные поля приложения

## PIEAPP_APPLICATION_NAME 
Возвращаемое значение: `<Lock[str]>`

Наименование приложения

<br>

## PIEAPP_APPLICATION_VERSION
Возвращаемое значение: `<Lock[str]>`

Версия приложения


<br>

## PIEAPP_ORGANIZATION_NAME 
Возвращаемое значение: `<Lock[str]>`

Наименование организации

<br>

## PIEAPP_ORGANIZATION_DOMAIN
Возвращаемое значение: `<Lock[str]>`

Домен организации

<br>

## PIEAPP_PROJECT_URL  
Возвращаемое значение: `<Lock[str]>`

Ссылка на проект

<br>

# Системные поля

## PIEKIT_VERSION 
Возвращаемое значение: `<Lock[str]>`

Версия `piekit`

<br>

## BASE_DIR
Возвращаемое значение: `<Lock[pathlib.Path]>`

Корневая директория

<br>

## APP_ROOT
Возвращаемое значение: `<Lock[pathlib.Path]>`

Корневая директория приложения (`pieapp`)

<br>

## SYSTEM_ROOT
Возвращаемое значение: `<Lock[pathlib.Path]>`

Корневая директория системы (`piekit`)

<br>

## USER_ROOT
Возвращаемое значение: `<Lock[pathlib.Path]>`

Корневая директория пользователя (`/home/user/` или `C:\Users\User`)

<br>

## DEFAULT_TEMP_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории временных файлов по-умолчанию

<br>

# Директории, файлы и поля ресурсов 

## PLUGINS_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории плагинов

<br>

## CONF_PAGES_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории модулей страниц настроек

<br>

## DEFAULT_PLUGIN_ICON_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование иконки плагина

<br>

# Директории, файлы и поля ресурсов

## ASSETS_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории ресурсов

<br>

## THEMES_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории ресурсов

<br>

## ICONS_ALLOWED_FORMATS
Возвращаемое значение: <list[str]>

Список разрешённых форматов иконок

<br>

## DEFAULT_THEME_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование темы по-умолчанию

<br>

## THEME_USE_STYLESHEET
Возвращаемое значение: `<Lock[bool]>`

Использовать ли каскадные таблицы стилей. По-умолчанию - `True`

<br>

# Директории, файлы и поля ресурсов 

## CONFIGS_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории конфигураций

<br>

## CONFIG_FILE_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование файла конфигураций

<br>

# Директории, файлы и поля ресурсов 

## LOCALES_FOLDER_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование директории файлов перевода

<br>


## DEFAULT_LOCALE_NAME
Возвращаемое значение: `<Lock[str]>`

Наименование локали по-умолчанию

<br>

## LOCALES_DICT
Возвращаемое значение: <dict[str, str]>

Словарь с доступными локализациями
