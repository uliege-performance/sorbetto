from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from sorbetto.core.importance import Importance


class AbstractFlavor(ABC):
    """
    A flavor is a function that gives something to show on a Tile for any given
    importance values.
    """

    def __init__(self, name: str = "Unnamed Flavor", colormap: Any = None):
        assert isinstance(name, str)
        self._name = name
        self._colormap = colormap
        ABC.__init__(self)

    @property
    def colormap(self) -> Any:
        if self._colormap is None:
            return self.getDefaultColormap()
        return self._colormap

    @colormap.setter
    def colormap(self, colormap: Any) -> None:
        self._colormap = colormap

    @abstractmethod
    def __call__(self, importance: Importance | np.ndarray) -> Any:
        """Computes the value of the flavor for the given importance value(s).


        Args:
            importance (Importance | np.ndarray): The importance value(s). Either a
                single Importance object or a numpy array of shape (..., 4), in which
                case the last dimension corresponds to (itn, ifp, ifn, itp).


        Returns:
            The value of the flavor evaluated at the given importance(s)
        """

    @abstractmethod
    def getDefaultColormap(self) -> Any: ...

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def __str__(self):
        return self.name
