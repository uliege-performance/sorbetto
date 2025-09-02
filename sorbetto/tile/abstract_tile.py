from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


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
        flavor: AbstractFlavor | None = None,
        resolution: int = 1001,
    ):
        """
        Args:
            parameterization (AbstractParameterization): The parameterization to be used
                for the tile.
            flavor (AbstractFlavor | None, optional): The flavor to use. Defaults to None.
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

        if flavor is not None:
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
    def importances(self):
        return self.parameterization.getCanonicalImportanceVectorized(
            self.sample_A, self.sample_B
        )

    @property
    def flavor(self) -> AbstractFlavor | None:
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
        self.sample_A, self.sample_B = np.meshgrid(a, b, indexing="xy")

    @abstractmethod
    def getExplanation(self) -> str: ...  # TODO

    # TODO: @abstractmethod ???
    def getParameterization(self) -> AbstractParameterization: ...  # TODO

    # TODO: @abstractmethod ???
    def getFlavor(self) -> AbstractFlavor: ...  # TODO

    def getResolution(self) -> int:
        return self.resolution

    def getVecParam1(self) -> np.ndarray:
        return (
            self.sample_A
        )  # TODO: self.sample_A does not exist. What is the meaning of A?

    def getVecParam2(self) -> np.ndarray:
        return (
            self.sample_B
        )  # TODO: self.sample_B does not exist. What is the meaning of B?

    # @abstractmethod
    # def getMat(self) -> np.ndarray: ...  # TODO

    # @abstractmethod
    # def getColormap(self) -> np.ndarray: ...  # TODO

    # annotations : List [ Annotation ]

    def genAnnotations(self):  # generator
        ...  # TODO

    def addAnnotation(self, annotation): ...  # TODO

    def delAnnotation(self, annotation): ...  # TODO

    def draw(self, fig: Figure | None = None, ax: Axes | None = None):
        """Draws the Tile in the given figure and axes.

        Args:
            fig (Figure | None, optional): The figure to draw in. If None, a new
                figure is created. Defaults to None.
            ax (Axes | None, optional): The axes to draw in. If None, a new axis is
                created. Defaults to None. Note that this argument is ignored if fig
                is None.


        Returns:
            The figure and axes used for drawing.
        """
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        parameterization = self.parameterization

        A = self.sample_A
        B = self.sample_B

        tile = self.compute_tile(A, B)

        if isinstance(
            self._flavor, AbstractNumericFlavor
        ):  # TODO: remove this (illogical)
            ax.imshow(
                tile,
                origin="lower",
                cmap=self._flavor.getDefaultColormap(),
                extent=(
                    self._flavor.getLowerBound(),
                    self._flavor.getUpperBound(),
                    self._flavor.getLowerBound(),
                    self._flavor.getUpperBound(),
                ),
                vmin=0.8,
                vmax=1.0,
            )

            fig.colorbar(ax.images[0], ax=ax)

        elif isinstance(
            self._flavor, AbstractSymbolicFlavor
        ):  # TODO: remove this (illogical)
            # FIXME and/or add stuff there
            ax.imshow(
                tile,
                origin="lower",
                # cmap=self._flavor.getDefaultColormap(),
            )

            # TODO add extent based on parametrization

        # TODO should be annotation

        ax.set_xlim(parameterization.getBoundsParameter1())
        ax.set_ylim(parameterization.getBoundsParameter2())
        ax.set_aspect("equal")
        ax.set_xlabel(parameterization.getNameParameter1())
        ax.set_ylabel(parameterization.getNameParameter2())
        ax.set_title(self.name)

        return fig, ax

    @abstractmethod
    def flavorCall(self, importance: np.ndarray) -> np.ndarray:
        """Calls the flavor.

        This function must be implemented in subclasses. The only argument is
        `importance`, which is a numpy array of shape ({{*self.resolution}}, 4)
        containing the sampled importances. Other arguments must be "hardcoded"
        directly in the subclass implementation of this function.
        """
        ...

    def compute_tile(
        self,
        param1: list[float] | np.ndarray | None = None,  # TODO: or float ?
        param2: list[float] | np.ndarray | None = None,  # TODO: or float ?
    ):  # uses `flavor ( importances )`.
        if not isinstance(param1, (np.ndarray)):
            param1 = np.array(param1)
        if not isinstance(param2, (np.ndarray)):
            param2 = np.array(param2)

        importance = self.parameterization.getCanonicalImportanceVectorized(
            param1, param2
        )

        if self.flavor is None:
            return np.zeros_like(importance.shape[:-1])

        return self.flavorCall(importance=importance)

    def __call__(self, param1: np.ndarray, param2: np.ndarray) -> np.ndarray:
        return self.compute_tile(param1, param2)

    def __str__(self) -> str:  # TODO
        return self.name
