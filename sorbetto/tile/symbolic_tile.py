# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.abstract_symbolic_flavor import AbstractSymbolicFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.tile.tile import Tile


class SymbolicTile(Tile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: AbstractSymbolicFlavor,
        name: str = "Symbolic Tile",
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, AbstractSymbolicFlavor)
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

    @property
    def flavor(self) -> AbstractSymbolicFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, AbstractSymbolicFlavor)
        return flavor

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
            vmin=0,  # TODO: 0.5 as the values are integers between 1 and codomain_size
            vmax=len(self.flavor.getCodomain())
            - 1,  # TODO: codomain_size + 0.5 as the values are integers between 1 and codomain_size
        )
        Tile.draw(self, fig, ax)
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
