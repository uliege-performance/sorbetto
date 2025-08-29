from abc import ABC, abstractmethod

from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class AbstractAnalysis(ABC):
    def __init__(
        self, parameterization: AbstractParameterization, resolution: int = 1001
    ):
        ABC.__init__(self)

        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )
        self._parameterization = parameterization

        if not isinstance(resolution, int):
            raise TypeError(f"resolution must be an integer, got {type(resolution)}")
        self._resolution = resolution

    @abstractmethod
    def genTiles(self):  # generator
        ...
