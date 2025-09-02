import numpy as np

from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.symbolic_tile import AbstractSymbolicTile
from sorbetto.tile.utils import get_colors


class EntityTile(AbstractSymbolicTile):
    def __init__(
        self,
        name: str,
        parameterization: AbstractParameterization,
        flavor: EntityFlavor,
        resolution: int = 1001,
    ):
        super().__init__(
            name=name,
            parameterization=parameterization,
            flavor=flavor,
            resolution=resolution,
        )
        self._rank = flavor._rank
        self._entities = flavor._entity_list
        self._colormap = get_colors(len(self._entities))
        self._performance = flavor._performances

        self.value_tile = None

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
