from piekit.managers.confpages.structs import ConfigurationPage
from piekit.managers.structs import Section


class TestPluginConfigurationPage(ConfigurationPage):
    category = Section.Root
    name = "test-configuration-page"
    title = "Test configuration page"

    def init(self) -> None:
        print("Hello!")

    def accept(self) -> None:
        print("Accepted")

    def cancel(self) -> None:
        print("Canceled")
