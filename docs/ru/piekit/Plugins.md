# Плагины

> Внимание: принцип работы может менятся в течении активной разработки проекта

<br>

## Описание
Плагины являются неотъемлемой частью приложения, выполняя роли полноценных микропрограмм, менеджеров, дополнением других плагинов и т.д.

<br>

## Регистрация и вызов плагинов
Для того, чтобы плагин был зарегистрирован, прежде всего его нужно создать. На данный момент это делается вручную.

В конечном итоге, у вас должна быть такая структура директории плагина:

## Корневая директория
![Корневая директория](../../images/plugin_folder1.png)

## Директория с ресурсами
![Директория ресурсов](../../images/plugin_folder2.png)

Откроем модуль `myplugin/plugin.py`

```py
from piekit.globals import Global
from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class MyPlugin(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "myplugin"

    def get_plugin_icon(self) -> "QIcon":
        raise NotImpelementedError("Method `get_plugin_icon` must be implemented")

    def init(self) -> None:
        raise NotImpelementedError("Method `init` must be implemented")


def main(*args, **kwargs) -> typing.Any:
    return MyPlugin(*args, **kwargs)
```

Но мы бы хотели, чтобы наш плагин что-нибудь делал.

Для начала переопределим метод `init`.

```py
def init(self) -> None:
    """
    Метод инициализации плагина
    """
    self.dialog = QDialog(self.parent())
    self.dialog.set_window_icon(self.get_plugin_icon())
    self.dialog.set_window_title(self.translate("My plugin"))

    self.button = QPushButton(self.translate("Ok"))
    self.button.clicked.connect(self.dialog.close)

    grid_layout = QGridLayout()
    grid_layout.add_widget(self.button, 0, 0)

    self.dialog.set_layout(grid_layout)
    self.dialog.resize(400, 300)
```

Переопределим метод `call`, чтобы мы могли вызывать окно при нажатии на кнопку в главном меню.

```py
def call(self) -> None:
    self.dialog.show()
```

Добавим немного логики в метод `main`

```py
def main(*args, **kwargs) -> typing.Any:
    """
    Метод настройки и запуска плагина
    """

    # Мы так же можем изменить значение поля конфигурации
    # Внимание! В этот момент это поле может не существовать
    # поэтому рекомендуется изменять их значения в методе `init`
    # или в методе, вызывающийся при доступности плагина, в котором
    # это поле объявлено
    Global.AUDIO_EXTENSIONS.append(".wav")

    # Запустим плагин
    return MyPlugin(*args, **kwargs)
```

Добавим кнопку в `MenuBar`:

```py
@on_plugin_event(target=Plugin.MenuBar)
def _on_menu_available_(self) -> None:
    self.add_menu_item(
        section=Sections.Shared,
        menu=Menus.Help,
        name="myplugin",
        text=self.translate("Dream plugin"),
        triggered=self.dialog.show,
        icon=self.get_plugin_icon(),
    )
```

Все готово! Теперь вы можете сделать свой плагин более замечательным!