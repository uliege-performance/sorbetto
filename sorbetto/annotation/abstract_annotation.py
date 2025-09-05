from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from matplotlib.axes import Axes
from matplotlib.figure import Figure

if TYPE_CHECKING:
    from sorbetto.tile.tile import Tile


class AbstractAnnotation(ABC):
    """
    This is the base class for all annotations, which are things that are drawn on top of Tiles.
    """

    def __init__(self, name: str | None = None):
        """
        Initializes a new annotation.

        Args:
            name (str | None, optional): the annotation name.
        """
        if name is None:
            name = "unnamed annotation"
        else:
            if not isinstance(name, str):
                name = str(name)
        self._name = name
        ABC.__init__(self)

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def draw(self, tile: "Tile", fig: Figure, ax: Axes) -> None:
        pass

    def __str__(self) -> str:
        return self.name
