from abc import ABC, abstractmethod

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class AbstractGeometricObject2D(ABC):
    def __init__(self, name=None):
        if name is None:
            name = "unnamed geometric object"
        elif not isinstance(name, str):
            name = str(name)
        self._name = name
        ABC.__init__(self)

    @abstractmethod
    def draw(self, fig: Figure, ax: Axes, extent, **plt_kwargs) -> None: ...

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name
