# Реестр менеджеров


# Описание
Данный реестр позволяет контролировать объекты, наследующие класс `BaseManager`. А именно: 
* монтирование объекта
* размонтирование объекта
* удаление объекта
* перезагрузка объекта
* вызов объекта


# Монтирование
Для добавления объекта в реестр можно использовать два способа: ручной и автоматическое


# Ручное добавление
Данный метод предпочтителен, чтобы самостоятельно проконтролировать запуск объекта и дальнейшего добавления в реестр. Пример использования:

```py
from piekit.system.manager import System
from pieapp.managers.mymanager.manager import MyManager

if <condition>: ...
    args = ...
    kwargs ...
    my_manager = MyManager()

System.registry.mount(my_manager, <args>, <kwargs>)

```

# Автоматическое добавление
Данный метод используется по-умолчанию и использует список менеджеров из системного конфигурационного модуля (`piekit/system/config.py`). 
Вы так же можете обновить данный список, чтобы загрузить свои менеджеры. 

```py
# pieapp/config.py
from piekit.system.types import EList
from piekit.system.types import ManagerConfig


MANAGERS: EList = [
    ManagerConfig(
        import_string="pieapp.managers.mymanager.manager.MyManager",
        mount=True,
        args=(...),
        kwargs={...}
    )
]


# pieapp/launcher.py
from piekit.system.manager import System

System.mount()
```

# Размонтирование, перезагрузка и удаление
Чтобы размонтировать, перезагрузить или удалить менеджер, нам нужно лишь вызвать метод `unmount/reload/delete` со списком 
наименований менеджеров или передать аргумент `full_house=True`, дабы перезагрузить всех менеджеров сразу. Пример использования:

```py
from piekit.system.manager import System

System.registry.unmount("configs", "locales", ...)

# Или

System.registry.unmount(full_house=True)
```