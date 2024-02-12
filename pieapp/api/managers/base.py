class BaseManager:
    """
    A very basic registry
    """
    name: str

    def init(self, *args, **kwargs) -> None:
        """
        Optional initializer
        """

    def shutdown(self):
        """
        This method serves to reset all containers, variables etc.
        Don't use it to delete data from memory
        """

    def reload(self):
        """
        This method reload manager
        """
        self.shutdown()
        self.init()

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) <name: {self.name}>"
