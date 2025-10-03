# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from sorbetto.core.named import Named
from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


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
        disable_legend: bool = False,
        base_constraint_on_importances: Any = None,
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, AbstractSymbolicFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0
        assert isinstance(disable_legend, bool)

        Tile.__init__(
            self,
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            base_constraint_on_importances=base_constraint_on_importances,
        )

        self._disable_legend = disable_legend

    @property
    def flavor(self) -> AbstractSymbolicFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, AbstractSymbolicFlavor)
        return flavor

    @property
    def disable_legend(self) -> bool:
        return self._disable_legend

    @disable_legend.setter
    def disable_legend(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f"disable_legend must be a bool, got {type(value)}")
        self._disable_legend = value

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
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
        Tile.draw(self, fig, ax)

        # im = ax.images[-1]
        # im.colorbar.set_ticks(range(min_value, max_value + 1))  # type: ignore

        if not self.disable_legend:

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

    def getExplanation(self) -> str:
        flavor_name = self.flavor.name
        parameterization = self.parameterization
        explanation = f"This Tile displays the flavor '{flavor_name}', with the parameterization '{parameterization.getName()}'."

        listing = [(symbol, self.getCoverage(symbol)) for symbol in self.listSymbols()]
        for symbol, coverage in sorted(listing, key=lambda element: element[1]):
            explanation += "\n - [{:6.3f} %] {}".format(100.0 * coverage, symbol)
        explanation += "\nBe aware that the coverage percentages given here-above are specific for the chosen parameterization."

        return explanation
