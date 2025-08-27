class AbstractFlavor(ABC):
    """
    A flavor is a function that gives something to show on a Tile for any given
    importance values.
    """

    def __init__(self, name=None):
        assert isinstance(name, (str, type(None)))
        self.name = name

    @abstractmethod
    def __call__(self, importances):
        pass

    @abstractmethod
    def getDefaultColormap(self):
        pass

    def getName(self):
        return self.name

    def __str__(self):
        return self.getName
