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
        entity_id: str | int,
        parameterization: AbstractParameterization,
        flavor: RankingFlavor,
        entities_list: list[Entity],
        resolution: int = 1001,
    ):
        if isinstance(entity_id, str):
            i = 0
            while i < len(entities_list):
                if entities_list[i].name == entity_id:
                    self._entity_id = entities_list[i].id
                    break
                i += 1

        elif isinstance(entity_id, int):
            self._entity_id = entity_id

        else:
            raise NotImplementedError(
                "Entity ID must be either a string or an integer."
            )

        self._colormap = get_colors(len(entities_list))
        self._performance = FiniteSetOfTwoClassClassificationPerformances(
            [ent.performance for ent in entities_list]
        )

        self.value_tile = None

        self._entities = entities_list

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
        return self.flavor(
            id_entity=self._entity_id,
            importance=importance,
            performance=self.performance,
        )

    def getExplanation(self):
        return "Explanation of the entity tile not yet defined"
