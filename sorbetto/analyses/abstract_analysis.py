from abc import ABC, abstractmethod

from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class AbstractAnalysis(ABC):
    def __init__(self, parameterization: AbstractParameterization, resolution=1001):
        ...  # TODO
        ABC.__init__(self)

    @abstractmethod
    def genTiles(self):  # generator
        ...
