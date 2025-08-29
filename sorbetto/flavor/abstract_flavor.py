from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from sorbetto.core.importance import Importance


class AbstractFlavor(ABC):
    """
    A flavor is a function that gives something to show on a Tile for any given
    importance values.
    """

    def __init__(self, name: str = "Default Flavor"):
        assert isinstance(name, str)
        self.name = name

    @abstractmethod
    def __call__(self, importance: Importance | np.ndarray, *args, **kwargs) -> Any: ...

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
