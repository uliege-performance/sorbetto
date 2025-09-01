from abc import abstractmethod

from sorbetto.flavor.abstract_flavor import AbstractFlavor


class AbstractSymbolicFlavor(AbstractFlavor):
    """
    A symbolic flavor is a function that gives something to show on a Tile for any
    given importance values.
    """

    def __init__(self, name: str = "Default Symbolic Flavor"):
        super().__init__(name)

    @abstractmethod
    def getCoDomain(self) -> set:
        pass
