# Типы данных

## Расширяемые типы данных
Нижеперечисленные типы данных используются в `ConfigLoader` для расширения конфигураций по-умолчанию.

* EList - Расширяемый список
* EDict - Расширяемый словарь

Пример использования. Допустим, у нас есть файлы конфигураций системы и приложения. В обоих файлах мы помечаем, что хотим расширить системный список компонентов за счёт тех, что находятся в конфигурации нашего приложения.:
```py
# Система
# system/config.py
COMPONENTS: EList = ["cloudykit.components.component.BuiltinComponent"]
```

```py
# Приложение
# %cloudyapp%/config.py
COMPONENTS: EList = ["cloudyapp.components.component.MyComponent"]
```

В результате мы получаем:
```py
>>> ["cloudykit.components.component.BuiltinComponent", "cloudyapp.components.component.MyComponent"]
```

> **Note**: Важно, чтобы аннотации переменных конфигураций были помечены как `EList`, `EDict` и т.д. Иначе они будут перезаписаны

## Прочие типы данных

## **DirectoryType**
Тип данных (флаг), обозначающий директорию. Используется в `AssetsManager` для игнорирования директорий при сборе ресурсов.
