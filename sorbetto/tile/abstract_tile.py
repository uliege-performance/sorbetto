from abc import ABC, abstractmethod

import numpy as np

from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.parameterization.parameterization_default import (
    ParameterizationDefault,
)  # TODO : it is not logical to have this import here.


class AbstractTile(ABC):
    """
    This is the base class for all Tiles.
    Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
    Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
    """

    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: AbstractFlavor,
        resolution: int = 1001,
    ):
        """
        Args:
            parameterization (AbstractParameterization): The parameterization to be used
                for the tile.
            flavor (AbstractFlavor): The flavor to use.
            resolution (int, optional): Resolution of the tile. Defaults to 1001.
            name (str | None, optional): Name of the tile. Defaults to None.

        Raises:
            TypeError: If the types of the arguments are incorrect.
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

        self._lower_bound, self._upper_bound = (
            self._parameterization.getBoundsParameter1()
        )

        self.update_grid()

    # TODO verify with parametrization bounds
    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value):
        self._lower_bound = value
        self.update_grid()

    @property
    def upper_bound(self):
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value):
        self._upper_bound = value
        self.update_grid()

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

    @resolution.setter
    def resolution(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"resolution must be an integer, got {type(value)}")
        self._resolution = value
        self.update_grid()

    def update_grid(self):
        a = np.linspace(self.lower_bound, self.upper_bound, self.resolution)
        b = np.linspace(self.lower_bound, self.upper_bound, self.resolution)
        self.sample_A, self.sample_B = np.meshgrid(a, b, indexing="ij")

    @abstractmethod
    def getExplanation(self) -> str: ...  # TODO

    # TODO: @abstractmethod ???
    def getParameterization(self) -> AbstractParameterization: ...  # TODO

    # TODO: @abstractmethod ???
    def getFlavor(self) -> AbstractFlavor: ...  # TODO

    @abstractmethod
    def getResolution(self) -> int: ...  # TODO

    @abstractmethod
    def getVecParam1(self) -> np.ndarray: ...  # TODO

    @abstractmethod
    def getVecParam2(self) -> np.ndarray: ...  # TODO

    @abstractmethod
    def getMat(self) -> np.ndarray: ...  # TODO

    @abstractmethod
    def getColormap(self) -> np.ndarray: ...  # TODO

    # annotations : List [ Annotation ]

    def genAnnotations(self):  # generator
        ...  # TODO

    def addAnnotation(self, annotation): ...  # TODO

    def delAnnotation(self, annotation): ...  # TODO

    @abstractmethod
    def draw(self, fig, ax): ...  # TODO

    def __call__(
        self,
        param1: list[float] | np.ndarray | None = None,  # TODO: or float ?
        param2: list[float] | np.ndarray | None = None,  # TODO: or float ?
        *args,
        **kwargs,
    ):  # uses `flavor ( importances )`.
        if not isinstance(param1, (np.ndarray)):
            param1 = np.array(param1)
        if not isinstance(param2, (np.ndarray)):
            param2 = np.array(param2)

        # TODO : should be self.getParameterization ().getCanonicalImportanceVectorized ...
        importances = ParameterizationDefault().getCanonicalImportanceVectorized(
            param1, param2
        )

        return self.flavor(importance=importances, *args, **kwargs)

    def __str__(self) -> str:  # TODO
        return self.name
