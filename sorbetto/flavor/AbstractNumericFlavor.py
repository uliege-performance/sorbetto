class AbstractNumericFlavor(AbstractFlavor):
    """
    A numeric flavor is a function that gives a real number to show on a Tile for any
    given importance values.
    """

    def __init__(self, name=None):
        assert isinstance(name, (str, type(None)))
        self.name = name

    @abstractmethod
    def getLowerBound(self):
        pass

    @abstractmethod
    def getUpperBound(self):
        pass
