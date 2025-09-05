from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


class NumericTile(Tile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractNumericFlavor,
        name: str = "Numeric Tile",
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        assert isinstance(flavor, AbstractNumericFlavor)
        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            disable_colorbar=disable_colorbar,
        )

        self._min: float | int | None = None
        self._max: float | int | None = None

    @property
    def min(self) -> float | int:
        if self._min is None:
            self._min = np.min(self.mat_value)
        return cast(float, self._min)

    @property
    def max(self) -> float | int:
        if self._max is None:
            self._max = np.max(self.mat_value)
        return cast(float, self._max)

    @property
    def flavor(self) -> AbstractNumericFlavor:
        return super().flavor  # type: ignore

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        # im =
        ax.imshow(
            self.mat_value,
            origin="lower",
            interpolation="bilinear",
            cmap=self.flavor.colormap,
            extent=self._zoom,  # extent is (left, right, bottom, top)
            vmin=self.flavor.getLowerBound(),
            vmax=self.flavor.getUpperBound(),
        )
        Tile.draw(self, fig, ax)
        return fig, ax

    def getExplanation(self) -> str:
        return "Sorry, we cannont provide yet an explanation for this Tile."
