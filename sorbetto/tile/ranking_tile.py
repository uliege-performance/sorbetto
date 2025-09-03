import numpy as np

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
        name: str,
        parameterization: AbstractParameterization,
        flavor: RankingFlavor,
        resolution: int = 1001,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
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

    def flavorCall(self, importance):
        assert self.flavor is not None
        return self.flavor(
            importance=importance,
        )

    def getExplanation(self):
        return "Explanation of the entity tile not yet defined"
