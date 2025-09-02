import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.flavor.ranking_flavor import RankingFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.abstract_numerical_tile import AbstractNumericalTile
from sorbetto.tile.utils import get_colors


class RankingTile(AbstractNumericalTile):
    def __init__(
        self,
        name: str,
        entity: Entity,
        parameterization: AbstractParameterization,
        flavor: RankingFlavor,
        entity_list: list[Entity],
        resolution: int = 1001,
    ):
        self._entities = entity_list

        for i, e in enumerate(self._entities):
            if e is entity:
                self._id_entity = i
                break
        else:
            raise ValueError("The given entity was not found in the given entity list.")

        self._colormap = get_colors(len(entity_list))
        self._performance = FiniteSetOfTwoClassClassificationPerformances(
            [ent.performance for ent in entity_list]
        )

        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )

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
