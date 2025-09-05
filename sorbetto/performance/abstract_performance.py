from abc import ABC, abstractmethod

import numpy as np


class AbstractPerformance(ABC):
    def __init__(self, name: str):
        self._name = name
        ABC.__init__(self)

    @abstractmethod
    def getMassFunction(self) -> np.ndarray: ...

    @property
    def name(self) -> str:
        return self._name
