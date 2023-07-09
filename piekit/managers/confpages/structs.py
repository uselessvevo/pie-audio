from piekit.config import PieException


class ConfigurationPage:
    category: str
    name: str
    title: str

    def init(self) -> None:
        """ Render page """
        raise PieException(f"Method `init` in \"{self.name}\" configuration page must be implemented")

    def accept(self) -> None:
        """ On accept event """
        raise PieException(f"Method `accept` in \"{self.name}\" configuration page must be implemented")

    def cancel(self) -> None:
        """ On cancel event """
        raise PieException(f"Method `cancel` in \"{self.name}\" configuration page must be implemented")

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}, category: {self.category}>"
