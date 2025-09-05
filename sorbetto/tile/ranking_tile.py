import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sorbetto.flavor.ranking_flavor import RankingFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.numeric_tile import NumericTile
from sorbetto.tile.utils import get_colors


class RankingTile(NumericTile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: RankingFlavor,
        name: str = "Ranking Tile",
        resolution: int = 1001,
        disable_colorbar: bool = False,
    ):
        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            disable_colorbar=disable_colorbar,
        )

        self._entities = self.flavor.entity_list
        self._performance = self.flavor.performances
        self._id_entity = self.flavor.id_entity

        # FIXME properly get colors from the Entities themselves
        self._colormap = get_colors(len(self._entities))

    @property
    def flavor(self) -> RankingFlavor:
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

    @rank.setter
    def rank(self, value: int):
        self._rank = value

    @property
    def performance(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performance

    @performance.setter
    def performance(self, value: FiniteSetOfTwoClassClassificationPerformances):
        self._performance = value

    def getExplanation(self):
        return "Explanation of the Ranking tile not yet defined"

    def draw(
        self, fig: Figure | None = None, ax: Axes | None = None
    ) -> tuple[Figure, Axes]:
        fig, ax = super().draw(fig, ax)

        im = ax.images[-1]
        im.set_clim(0.5, self.flavor.nb_entities + 0.5)
        if im.colorbar is not None:
            im.colorbar.set_ticks([1, self.flavor.nb_entities])
            im.colorbar.set_label("Rank from {} to {}".format(self.min, self.max))
        return fig, ax
