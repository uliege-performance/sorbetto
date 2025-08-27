class AbstractFlavor(ABC):
    """
    A flavor is a function that gives something to show on a Tile for any given importance values.
    """

    def __init__(self, name=None):
        return

    @abstractmethod
    def __call__(self, importances):
        return

    @abstractmethod
    def getDefaultColormap(self):
        return

    def getName(self):
        return

    def __str__(self):
        return
