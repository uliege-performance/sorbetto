from abc import abstractmethod
from typing import Any

from sorbetto.flavor.abstract_flavor import AbstractFlavor


class AbstractSymbolicFlavor(AbstractFlavor):
    """
    A symbolic flavor is a function that gives something to show on a Tile for any
    given importance values.
    """

    def __init__(self, name: str = "Unnamed Symbolic Flavor", colormap: Any = None):
        super().__init__(name=name, colormap=colormap)

    @abstractmethod
    def getCodomain(self) -> set:
        """Returns the codomain of the flavor.
        See https://en.wikipedia.org/wiki/Codomain

        Returns:
            The codomain of the flavor.
        """
        pass
