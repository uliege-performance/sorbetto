from abc import ABC, abstractmethod

import numpy as np

from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class AbstractTile(ABC):
    """
    This is the base class for all Tiles.
    Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
    Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractFlavor,
        resolution: int = 1001,
        name: str | None = None,
    ):
        """
        Args:
            parameterization (AbstractParameterization): _description_
            flavor (AbstractFlavor): _description_
            resolution (int, optional): _description_. Defaults to 1001.
            name (str | None, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_
        """
        if not isinstance(parameterization, AbstractParameterization):
            raise TypeError(
                f"parameterization must be an instance of AbstractParameterization, got {type(parameterization)}"
            )
        self._parameterization = parameterization

        if not isinstance(flavor, AbstractFlavor):
            raise TypeError(
                f"flavor must be an instance of AbstractFlavor, got {type(flavor)}"
            )
        self._flavor = flavor

        if not isinstance(resolution, int):
            raise TypeError(f"resolution must be an integer, got {type(resolution)}")
        self._resolution = resolution

        self.name = name
        # other args
        ...  # TODO

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = "Default name"
        elif not isinstance(value, str):
            value = str(value)
        self._name = value

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
