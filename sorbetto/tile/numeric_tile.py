# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import logging
import math
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.colors import Colormap, ListedColormap
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


class NumericTile(Tile):
    """
    By default, Numeric Tiles are displayed with a colorbar.
    """

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
        assert isinstance(disable_colorbar, bool)

        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
        )

        self._disable_colorbar = disable_colorbar

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
            self._min = np.nanmin(self.mat_value)
        return cast(float, self._min)

    @property
    def max(self) -> float | int:
        """
        Returns:
            float | int: the maximal value on the grid of precomputed values
        """
        if self._max is None:
            self._max = np.nanmax(self.mat_value)
        return cast(float, self._max)

    @property
    def disable_colorbar(self) -> bool:
        return self._disable_colorbar

    @disable_colorbar.setter
    def disable_colorbar(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f"disable_colorbar must be a bool, got {type(value)}")
        self._disable_colorbar = value

    def _optimize(
        self, scale: float, precision: float = 1e-6
    ) -> tuple[float, float, float]:
        assert isinstance(scale, float)
        assert math.isfinite(scale)
        assert isinstance(precision, float)
        assert precision > 0.0

        parameterization = self._parameterization

        def objective(x: np.ndarray):
            assert x.size == 2
            importance = parameterization.getCanonicalImportance(x[0], x[1])
            return scale * self._flavor(importance)

        x_min, x_max, y_min, y_max = parameterization.getExtent()

        # TODO: try several times, starting from randomly chosen points,
        # and keep the best result at the end.

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

        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(v, float)

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

    @staticmethod
    def _clampColormap(
        *,
        colormap: Colormap | str,
        min_val: float,
        max_val: float,
        clamped_min_val: float,
        clamped_max_val: float,
    ) -> ListedColormap:
        assert isinstance(colormap, (Colormap, str))
        assert isinstance(min_val, float)
        assert isinstance(max_val, float)
        assert isinstance(clamped_min_val, float)
        assert isinstance(clamped_max_val, float)
        assert math.isfinite(min_val)
        assert math.isfinite(max_val)
        assert math.isfinite(clamped_min_val)
        assert math.isfinite(clamped_max_val)
        assert min_val < max_val
        assert clamped_min_val <= clamped_max_val

        clamped_min_val = min(max(clamped_min_val, min_val), max_val)
        clamped_max_val = min(max(clamped_max_val, min_val), max_val)

        # Be sure that the clamped interval is large enough to be visible in the colormap.
        clamped_delta = clamped_max_val - clamped_min_val
        min_clamped_delta = (max_val - min_val) / 100.0
        if clamped_delta < min_clamped_delta:
            clamped_center = 0.5 * (clamped_min_val + clamped_max_val)
            min_clamped_center = min_val + 0.5 * min_clamped_delta
            max_clamped_center = max_val - 0.5 * min_clamped_delta
            clamped_center = min(
                max(clamped_center, min_clamped_center),
                max_clamped_center,
            )
            clamped_min_val = clamped_center - 0.5 * min_clamped_delta
            clamped_max_val = clamped_center + 0.5 * min_clamped_delta

        if isinstance(colormap, str):
            # Let's assume it is the name of a standard colormap in matplotlib
            colormap = cm.get_cmap(colormap, 2048)
            # 2048 is an arbitrary number but hugh to have a smooth colormap
            colormap.set_bad("black")
            colormap.set_over("black")
            colormap.set_under("black")
        else:
            assert isinstance(colormap, Colormap)
        N = colormap.N
        colors = colormap(np.linspace(0, 1, N))
        background_color = np.array([256 / 256, 256 / 256, 256 / 256, 1])  # RGBA

        relative_value = (clamped_min_val - min_val) / (max_val - min_val)
        idx = math.floor(relative_value * (N - 1))
        if idx != 0:
            colors[: idx - 1, :] = background_color

        relative_value = (clamped_max_val - min_val) / (max_val - min_val)
        idx = math.ceil(relative_value * (N - 1))
        if idx != N - 1:
            colors[idx + 1 :, :] = background_color

        clamped_colormap = ListedColormap(colors)
        clamped_colormap.set_bad(colormap.get_bad())
        clamped_colormap.set_over(colormap.get_over())
        clamped_colormap.set_under(colormap.get_under())
        return clamped_colormap

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        min_val = self.flavor.getLowerBound()
        max_val = self.flavor.getUpperBound()

        try:
            # Compute bounds for the value:
            # [self.min, self.max] is obtained on a grid
            # [self.minimize(), self.maximize()] is obtained by optimization
            _, _, minimized_value = self.minimize()
            _, _, maximized_value = self.maximize()
            clamped_min_val = min(self.min, minimized_value)
            clamped_max_val = max(self.max, maximized_value)
        except Exception as e:
            logging.warning(
                f"Impossible to determine the range of values to clamp the colormap: {e}"
            )
            # Do not clamp.
            clamped_min_val = min_val
            clamped_max_val = max_val

        colormap = self._clampColormap(
            colormap=self.flavor.colormap,
            min_val=min_val,
            max_val=max_val,
            clamped_min_val=clamped_min_val,
            clamped_max_val=clamped_max_val,
        )

        ax.imshow(
            self.mat_value,
            origin="lower",
            extent=self._zoom,  # extent is (left, right, bottom, top)
            interpolation="bilinear",
            cmap=colormap,
            vmin=min_val,
            vmax=max_val,
        )
        Tile.draw(self, fig, ax)

        if not self.disable_colorbar:
            # Create a subdivision of the axis to add a colorbar of same height
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad="5%")
            fig.colorbar(
                ax.images[0], cax, label=self.flavor.name
            )  # TODO: make sure this works with a base (empty) Tile?

        return fig, ax

    def getExplanation(self) -> str:
        return "Sorry, we cannont provide yet an explanation for this Tile."
