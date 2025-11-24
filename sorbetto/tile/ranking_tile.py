# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

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
        colorbar_mode: str = "default",
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, RankingFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0

        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            colorbar_mode=colorbar_mode,
            base_constraint_on_importances=None,
        )

        self._entities = self.flavor.entity_list
        self._performance = self.flavor.performances
        self._id_entity = self.flavor.id_entity

        # FIXME properly get colors from the Entities themselves
        self._colormap = get_colors(len(self._entities))

    @property
    def flavor(self) -> RankingFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, RankingFlavor)
        return flavor

    @property
    def entities(self):
        return self._entities

    @property
    def colormap(self) -> np.ndarray:
        # TODO: Why is it in this class? Should'nt it be is class Tile?
        return self._colormap

    @colormap.setter
    def colormap(self, value: np.ndarray):
        # TODO: Why is it in this class? Should'nt it be is class Tile?
        self._colormap = value

    @property
    def performance(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performance

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

    def getExplanation(self):
        return "Explanation of the Ranking tile not yet defined"
