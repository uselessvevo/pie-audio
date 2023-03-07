# Plugins

# Registraion and render
In *piekit*, almost all visual components are plugins. This means that the `MenuBar`, `Workbench` (toolbar) and etc. are plugins. 
Event more, they are "not nailed" to each other.

For example, to register and render your plugin on the `MenuBar`, you need to use the `MenuBarAccessor` mixin:


```py
# pieapp/plugins/about-app

@onPluginAvailable(target=Containers.MenuBar)
def onMenuBarAvailable(self) -> None:
    self.addMenuItem(
        section=Sections.Shared,
        menu=Menus.Help,
        name="about",
        text=self.getTranslation("About"),
        triggered=self.dialog.show,
        icon=self.getAssetIcon("help.png"),
    )
```

This mixin also will add the menu item into the menu registry (`MenuManager`).
