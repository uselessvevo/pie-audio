# Системный менеджер


# Описание
Основное назначение данного менеджера - упрощённый доступ к менеджерам и прочим службам, подключаемых через реестры объектов (к примеру, `ManagersRegistry`). 
Дополнительно этот менеджер решает проблему с рекурсивным импортом.

Содержит в себе:
* Реестр менеджеров - `ManagersRegistry / registry`
* Загрузчик конфигураций - `ConfigLoader / config`
* Информацию о расположении приложения корневой директории - `APP_ROOT / root`
* Модуль журналирования (логер) - `logging.logger / logger`


# Примеры использования

Обращение к конфигурации

```py
>>> from cloudtykit.system.manager import System
>>> str(System.config.USER_CONFIGS_FOLDER / "directory name")
>>> "/path/to/cloudyff/directory/directory name"
```

Обращение к менеджеру
```py
>>> from cloudtykit.system.manager import System
# Получаем экземпляр класса `LocalesManager`
>>> System.registry.locales("Username")
>>> "Имя пользователя"
```
