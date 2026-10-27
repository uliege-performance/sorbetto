# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from skimage.measure import find_contours

from sorbetto.core import Named
from sorbetto.flavor import AbstractSymbolicFlavor
from sorbetto.parameterization import (
    AbstractParameterization,
)
from sorbetto.ranking import Importance

from ._tile import Tile


class SymbolicTile(Tile):
    """
    By default, Symbolic Tiles are displayed with a legend.
    """

    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        name: str = "Symbolic Tile",
        resolution: int = 1001,
        legend_mode: str = "default",  # legend is outside, on the right, and the labels are cut at 30 characters.
        base_constraint_on_importances: Any = None,
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, AbstractSymbolicFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0
        assert isinstance(legend_mode, str)

        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            base_constraint_on_importances=base_constraint_on_importances,
        )

        self._legend_mode = legend_mode

    @property
    def flavor(self) -> AbstractSymbolicFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, AbstractSymbolicFlavor)
        return flavor

    @property
    def legend_mode(self) -> str:
        return self._legend_mode

    @legend_mode.setter
    def legend_mode(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"legend_mode must be a str, got {type(value)}")
        self._legend_mode = value

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None, **kwargs
    ) -> tuple[Figure, Axes]:
        if fig is None:
            fig = plt.figure()
            ax = fig.gca()
        elif ax is None:
            ax = fig.gca()

        num_symbols = len(self.flavor.getCodomain())
        min_value = 1  # this has been chosen in the mapper in SymbolicFlavor
        max_value = num_symbols  # this has been chosen in the mapper in SymbolicFlavor

        # im =
        ax.imshow(
            self.mat_value,
            origin="lower",
            interpolation="none",
            cmap=self.flavor.colormap,
            extent=self._zoom,  # extent is (left, right, bottom, top)
            vmin=min_value - 0.5,
            vmax=max_value + 0.5,
        )
        Tile.draw(self, fig, ax, **kwargs)

        # im = ax.images[-1]
        # im.colorbar.set_ticks(range(min_value, max_value + 1))  # type: ignore

        if self.legend_mode != "off":

            def getLegendElement(symbol):
                max_label_size = 30  # >= 4
                if isinstance(symbol, Named):
                    label = symbol.name
                else:
                    label = str(symbol)
                if len(label) > max_label_size:
                    label = label[: max_label_size - 4] + " ..."
                value = self.flavor.mapper(symbol)
                color = self.flavor.colormap(value - 1)  # TODO: why -1 ?
                return Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    label=label,
                    markerfacecolor=color,
                    markersize=10,
                )

            legend_elements = [
                getLegendElement(symbol) for symbol in self.listSymbols()
            ]

            ax.legend(
                handles=legend_elements,
                bbox_to_anchor=(1.05, 0.5),
                loc="center left",
                borderaxespad=0,
                ncols=1 + (len(legend_elements) - 1) / 18,
            )

        return fig, ax

    def listSymbols(self) -> list:
        mat_value = self._mat_value
        values = np.unique(mat_value)
        ans = list()
        for value in values:
            symbol = self.flavor.reverse_mapper(value)
            ans.append(symbol)
        return ans

    def getCoverage(self, symbol) -> float:
        flavor = self.flavor
        assert symbol in flavor.getCodomain()
        value = flavor.mapper(symbol)
        return np.mean(self.mat_value == value)

    def getCanonicalImportancesForContours(self, symbol) -> list[list[Importance]]:
        canonical_importance_contours = list()

        mat_value = self.mat_value
        vec_x = self._vec_x
        vec_y = self._vec_y

        w = np.size(vec_x)
        h = np.size(vec_y)

        vec_col = np.linspace(0, w - 1, w)
        vec_row = np.linspace(0, h - 1, h)

        flavor = self.flavor
        assert symbol in flavor.getCodomain()
        value = flavor.mapper(symbol)
        bininarized = mat_value == value
        contours = find_contours(bininarized, level=0.5)
        for contour in contours:
            canonical_importance_contour = list()
            assert isinstance(contour, np.ndarray)
            assert np.ndim(contour == 2)
            shape = np.shape(contour)
            num_verticies = shape[0]
            assert shape[1] == 2
            for vertex_idx in range(num_verticies):
                row = contour[vertex_idx, 0]
                col = contour[vertex_idx, 1]
                x = np.interp(col, vec_col, vec_x)
                y = np.interp(row, vec_row, vec_y)
                canonical_importance = self.parameterization.getCanonicalImportance(
                    x, y
                )
                canonical_importance_contour.append(canonical_importance)
            canonical_importance_contours.append(canonical_importance_contour)

        return canonical_importance_contours

    def getExplanation(self) -> str:
        flavor_name = self.flavor.name
        parameterization = self.parameterization
        explanation = f"This Tile displays the flavor '{flavor_name}', with the parameterization '{parameterization.getName()}'."

        listing = [(symbol, self.getCoverage(symbol)) for symbol in self.listSymbols()]
        for symbol, coverage in sorted(listing, key=lambda element: element[1]):
            explanation += "\n - [{:6.3f} %] {}".format(100.0 * coverage, symbol)
        explanation += "\nBe aware that the coverage percentages given here-above are specific for the chosen parameterization."

        return explanation
