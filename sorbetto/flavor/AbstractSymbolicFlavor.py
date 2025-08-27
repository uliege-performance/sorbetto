class AbstractSymbolicFlavor(AbstractFlavor):
    """
    A symbolic flavor is a function that gives something to show on a Tile for any
    given importance values.
    """

    def __init__(self, name=None):
        assert isinstance(name, (str, type(None)))
        self.name = name

    @abstractmethod
    def getCodomain(self) -> set:
        pass
