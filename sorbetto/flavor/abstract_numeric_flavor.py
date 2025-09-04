from abc import abstractmethod
from typing import Any

from sorbetto.flavor.abstract_flavor import AbstractFlavor


class AbstractNumericFlavor(AbstractFlavor):
    """
    A numeric flavor is a function that gives a real number to show on a Tile for any
    given importance values.
    """

    def __init__(self, name: str = "Unnamed Numeric Flavor", colormap: Any = None):
        super().__init__(name=name, colormap=colormap)

    @abstractmethod
    def getLowerBound(self) -> Any: ...

    @abstractmethod
    def getUpperBound(self) -> Any: ...

    @property
    def lowerBound(self):
        return self.getLowerBound()

    @property
    def upperBound(self):
        return self.getUpperBound()
