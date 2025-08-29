from abc import ABC, abstractmethod

import numpy as np

from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.parametrization.abstract_parametrization import AbstractParametrization


class AbstractTile(ABC):
    """
    This is the base class for all Tiles.
    Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
    Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
    """

    def __init__(
        self,
        parametrization: AbstractParametrization,
        flavor: AbstractFlavor,
        resolution: int = 1001,
        name: str | None = None,
    ):
        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"paramer must be an instance of Importance, got {type(importance)}"
            )

        self._name = name
        self._parameterization = parameterization
        self._flavor = flavor
        self._resolution = resolution
        # other args
        ...  # TODO

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameterization(self) -> AbstractParameterization:
        return self._parameterization

    @property
    def flavor(self) -> AbstractFlavor:
        return self._flavor

    @property
    def resolution(self) -> int:
        return self._resolution

    @abstractmethod
    def getExplanation(self) -> str: ...  # TODO

    def getParameterization(self) -> AbstractParameterization: ...  # TODO

    def getFlavor(self) -> AbstractFlavor: ...  # TODO

    def getResolution(self) -> int: ...  # TODO

    def getVecParam1(self) -> np.ndarray: ...  # TODO

    def getVecParam2(self) -> np.ndarray: ...  # TODO

    def getMat(self) -> np.ndarray: ...  # TODO

    def getColormap(self) -> np.ndarray: ...  # TODO

    # annotations : List [ Annotation ]

    def genAnnotations(self):  # generator
        ...  # TODO

    def addAnnotation(self, annotation): ...  # TODO

    def delAnnotation(self, annotation): ...  # TODO

    @abstractmethod
    def draw(self, fig, ax): ...  # TODO

    def __call__(self, param1, param2):  # uses `flavor ( importances )`.
        ...  # TODO

    def __str__(self) -> str: ...  # TODO
