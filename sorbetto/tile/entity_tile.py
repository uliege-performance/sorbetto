import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.symbolic_tile import SymbolicTile


class EntityTile(SymbolicTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: EntityFlavor,
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
            disable_colorbar=disable_colorbar,
        )
        self._rank = self.flavor.rank
        self._entities = self.flavor.entity_list
        self._colormap = self.flavor.colormap
        self._performance = self.flavor.performances

        self.value_tile = None

    @property
    def flavor(self) -> EntityFlavor:
        return super().flavor  # type: ignore

    @property
    def entities(self):
        return self._entities

    @property
    def colormap(self) -> np.ndarray:
        return self._colormap

    @colormap.setter
    def colormap(self, value: np.ndarray):
        self._colormap = value

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def performance(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performance

    def getExplanation(self):
        return "Explanation of the entity tile not yet defined"

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        fig, ax = super().draw(fig, ax)

        im = ax.images[-1]
        im.set_clim(0.5, self.flavor.nb_entities + 0.5)
        im.colorbar.set_ticks(range(1, self.flavor.nb_entities + 1))  # type: ignore

        return fig, ax
