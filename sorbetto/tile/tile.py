import io
import logging
from typing import Iterator, SupportsIndex, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from sorbetto.annotation.abstract_annotation import AbstractAnnotation
from sorbetto.core.types import Extent
from sorbetto.flavor.abstract_flavor import AbstractFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization


class Tile:
    """
    This is the base class for all Tiles. A Tile is a graphical representation (of what ????) with:
    - a parameterization;
    - a flavor; # TDOO: not always because of EmptyTile
    - and some annotations.

    Tiles with the default parameterization are studied in detail in :cite:t:`Pierard2024TheTile-arxiv`.
    Various flavors of Tiles are described in :cite:t:`Halin2024AHitchhikers-arxiv` and :cite:t:`Pierard2025AMethodology`.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractFlavor | None = None,
        name: str = "Tile",
        resolution: int = 1001,
        disable_colorbar: bool = True,
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

        self._name = name

        if (not isinstance(resolution, int)) or resolution <= 0:
            raise TypeError(
                f"resolution must be a strictly positive integer, got {resolution!r}"
            )
        self._resolution = resolution

        self._zoom = self._parameterization.getExtent()

        self._mat_value: np.ndarray | None = None
        self._update_grid()

        self._annotations: list[AbstractAnnotation] = list()

        self._disable_colorbar = disable_colorbar

    @property
    def resolution(self) -> int:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: int):
        if (not isinstance(resolution, int)) or resolution <= 0:
            raise TypeError(
                f"resolution must be a strictly positive integer, got {resolution!r}"
            )
        self._resolution = resolution
        self._update_grid()

    @property
    def zoom(self) -> Extent:
        return self._zoom

    @zoom.setter
    def zoom(self, zoom: Extent):
        def intersection(extent_1: Extent, extent_2: Extent) -> Extent:
            min_x_1, max_x_1, min_y_1, max_y_1 = extent_1
            assert min_x_1 < max_x_1
            assert min_y_1 < max_y_1
            min_x_2, max_x_2, min_y_2, max_y_2 = extent_2
            assert min_x_2 < max_x_2
            assert min_y_2 < max_y_2
            min_x = max(min_x_1, min_x_2)
            max_x = min(max_x_1, max_x_2)
            min_y = max(min_y_1, min_y_2)
            max_y = min(max_y_1, max_y_2)
            assert min_x < max_x
            assert min_y < max_y
            return (min_x, max_x, min_y, max_y)

        assert isinstance(zoom, tuple)
        assert len(zoom) == 4
        assert all(isinstance(v, float) for v in zoom)
        extent = self._parameterization.getExtent()
        self._zoom = intersection(zoom, extent)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            value = "Unnamed Tile"
        elif not isinstance(value, str):
            value = str(value)
        self._name = value

    @property
    def parameterization(self) -> AbstractParameterization:
        return self._parameterization

    @property
    def importances(self):
        return self.parameterization.getCanonicalImportanceVectorized(
            self._mat_x, self._mat_y
        )

    @property
    def flavor(self) -> AbstractFlavor | None:
        return self._flavor

    @property
    def disable_colorbar(self) -> bool:
        return self._disable_colorbar

    @disable_colorbar.setter
    def disable_colorbar(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f"disable_colorbar must be a bool, got {type(value)}")
        self._disable_colorbar = value

    def _update_grid(self):
        x_min, x_max, y_min, y_max = self._zoom
        assert x_min < x_max
        assert y_min < y_max
        vec_x = np.linspace(x_min, x_max, self.resolution)
        self._vec_x = vec_x
        vec_y = np.linspace(y_min, y_max, self.resolution)
        self._vec_y = vec_y
        self._mat_x, self._mat_y = np.meshgrid(vec_x, vec_y, indexing="xy")
        self._mat_value = None

    def getExplanation(self) -> str:
        return self.__str__()

    @property
    def mat_value(self) -> np.ndarray:
        if self._flavor is None:
            tmp = np.empty([self.resolution, self.resolution])
            tmp[:] = np.nan
            return tmp
        if self._mat_value is None:
            self._mat_value = self._compute_mat_value(self._mat_x, self._mat_y)
        return cast(np.ndarray, self._mat_value)

    def _compute_mat_value(
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

        return self.flavor(importance=importance)

    def __call__(self, param1: np.ndarray, param2: np.ndarray) -> np.ndarray:
        return self._compute_mat_value(param1, param2)

    # @abstractmethod
    # def getColormap(self) -> np.ndarray: ...  # TODO

    def genAnnotations(self) -> Iterator[AbstractAnnotation]:  # Generator
        for annotation in self._annotations:
            yield annotation

    def appendAnnotation(self, annotation):
        assert isinstance(annotation, AbstractAnnotation)
        self._annotations.append(annotation)

    def removeAnnotation(self, annotation):
        assert isinstance(annotation, AbstractAnnotation)
        self._annotations.remove(annotation)

    def popAnnotation(self, index: SupportsIndex = -1) -> AbstractAnnotation:
        """
        Remove and return an annotation at index (default last).

        Args:
            index (SupportsIndex, optional): index of the annotation to pop. Defaults to -1.

        Returns:
            AbstractAnnotation: the annotation at the specified index.

        Raises:
            IndexError: if the index is out of range.
        """
        return self._annotations.pop(index)

    def clearAnnotations(self):
        self._annotations.clear()

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
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

        # Draw all annotations

        for annotation in self.genAnnotations():
            assert isinstance(annotation, AbstractAnnotation)
            tile = self
            try:
                annotation.draw(tile, fig, ax)
            except Exception as e:
                message = (
                    "Something went wrong while drawing annotation {!r}, got {}".format(
                        annotation.name, e
                    )
                )
                logging.warning(message)

        # Configure the limits, axes labels, and title.

        x_min, x_max, y_min, y_max = self._zoom
        assert x_min < x_max
        assert y_min < y_max

        ax.set_xlim((x_min, x_max))
        ax.set_ylim((y_min, y_max))
        ax.set_aspect("equal")
        parameterization = self.parameterization
        ax.set_xlabel(parameterization.getNameParameter1())
        ax.set_ylabel(parameterization.getNameParameter2())
        ax.set_title(self.name)

        if not self.disable_colorbar:
            # Create a subdivision of the axis to add a colorbar of same height
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad="5%")
            fig.colorbar(ax.images[0], cax)

        return fig, ax

    def __str__(self) -> str:
        buffer = io.StringIO()
        buffer.write('This Tile is named "{}".'.format(self.name))
        buffer.write("\nIt uses the flavor: {}.".format(self.flavor))
        buffer.write(
            "\nIt uses the parameterization: {}.".format(self.parameterization)
        )
        if len(self._annotations) > 0:
            buffer.write("\nIt shows the following annotations:\n")
            for annotation in self._annotations:
                buffer.write("- {}\n".format(annotation.name))
        return buffer.getvalue()
