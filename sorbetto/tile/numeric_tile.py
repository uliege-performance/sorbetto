# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import scipy
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
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, AbstractNumericFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0

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
    def flavor(self) -> AbstractNumericFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, AbstractNumericFlavor)
        return flavor

    @property
    def min(self) -> float | int:
        """
        Returns:
            float | int: the minimal value on the grid of precomputed values
        """
        if self._min is None:
            self._min = np.min(self.mat_value)
        return cast(float, self._min)

    @property
    def max(self) -> float | int:
        """
        Returns:
            float | int: the maximal value on the grid of precomputed values
        """
        if self._max is None:
            self._max = np.max(self.mat_value)
        return cast(float, self._max)

    def _optimize(
        self, scale: float, precision: float = 1e-6
    ) -> tuple[float, float, float]:
        assert isinstance(precision, float)
        assert precision > 0.0

        parameterization = self._parameterization

        def objective(x: np.ndarray):
            assert x.size() == 2
            importance = parameterization.getCanonicalImportance(x[0], x[1])
            return scale * self._flavor(importance)

        x_min, x_max, y_min, y_max = parameterization.getExtent()
        center_x = 0.5 * (x_min + x_max)
        center_y = 0.5 * (y_min + y_max)
        start = np.asarray([center_x, center_y])

        bounds = [[x_min, x_max], [y_min, y_max]]

        output = scipy.optimize.minimize(
            objective, start, method="SLSQP", bounds=bounds, tol=precision
        )  # TODO: specify the gradient when it is possible to know it.
        if not output.success:
            message = "scipy.optimize.minimize did not succeed: " + output.message
            logging.warning(message)
        x = output.x[0]
        y = output.x[1]
        i = parameterization.getCanonicalImportance(x, y)
        v = self._flavor(i)
        return x, y, v

    def minimize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        """
        Minimization of the flavor over the Tile. The default implementation
        does it by gradient descent.

        Args:
            precision (float, optional): tolerance for termination. Defaults to 1e-6.

        Returns:
            tuple[float, float, float]:
            - float: the first coordinate of the point on the Tile where the smallest value has been found.
            - float: the second coordinate of the point on the Tile where the smallest value has been found.
            ) float: the smallest value that has been found.
        """
        return self._optimize(1.0, precision)

    def maximize(self, precision: float = 1e-6) -> tuple[float, float, float]:
        """
        Maximization of the flavor over the Tile. The default implementation
        does it by gradient descent.

        Args:
            precision (float, optional): tolerance for termination. Defaults to 1e-6.

        Returns:
            tuple[float, float, float]:
            - float: the first coordinate of the point on the Tile where the largest value has been found.
            - float: the second coordinate of the point on the Tile where the largest value has been found.
            ) float: the largest value that has been found.
        """
        return self._optimize(-1.0, precision)

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
