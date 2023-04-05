# Плагины

# Описание
В `piekit` имеется поддержка плагинов и чтобы создать плагин мечты, для начала определим, какой именно тип плагина вам нужен - контейнер или приложение?

**Контейнер** - это плагин, который предусматривает регистрацию других плагинов (приложений) на себе.

**Приложение** - это независимый от других плагин, не предусматривающий регистрацию.

Для начала создадим директорию `plugins/<your plugin name>` в проекте или в директории пользователя, используя `pie-cli.py`.

```
pie-cli.py --create-plugin dream-plugin --folder plugin/container
```

Так же, вы можете указать дополнительные параметры для создания директорий:

```
... --add-configs --add-locales --add-assets
```

Структура директории плагина:

```
plugins/
... dream-plugin/
...... assets
...... configs
...... locales
...... plugin /
............ plugin.py
............ confpage.py
............ widget.py
...... __init__.py
...... app.png
```

Откроем модуль `plugin/plugin.py`


```py
import typing

from piekit.plugins.plugins import PiePlugin
from piekit.managers.assets.mixins import AssetsAccessor
from piekit.managers.configs.mixins import ConfigAccessor
from piekit.managers.locales.mixins import LocalesAccessor


class DreamPlugin(
    PiePlugin,
    ConfigAccessor,
    LocalesAccessor,
    AssetsAccessor,
):
    name = "dream-plugin"

    def init(self) -> None:
        raise NotImpelementedError("Method `init` must be implemented")


def main(*args, **kwargs) -> typing.Any:
    return DreamPlugin(*args, **kwargs)
```

Но мы бы хотели, чтобы наш плагин что-нибудь делал и чтобы мы могли его запустить.

Переопределим метод `init`:

```py
def init(self) -> None:
    self.dialog = QDialog(self.parent())
    self.dialog.setWindowIcon(self.getAssetIcon("help.png"))
    self.dialog.setWindowTitle(self.getTranslation("Dream plugin"))

    self.button = QPushButton(self.getTranslation("Ok"))
    self.button.clicked.connect(self.dialog.close)

    gridLayout = QGridLayout()
    gridLayout.addWidget(self.button, 0, 0)

    self.dialog.setLayout(gridLayout)
    self.dialog.resize(400, 300)
```

Добавим кнопку в `MenuBar`:

```py
@onPluginAvailable(target=Containers.MenuBar)
def onMenuBarAvailable(self) -> None:
    self.addMenuItem(
        section=Sections.Shared,
        menu=Menus.Help,
        name="dream",
        text=self.getTranslation("Dream plugin"),
        triggered=self.dialog.show,
        icon=self.getAssetIcon("help.png"),
    )
```