import numpy as np

from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.symbolic_tile import SymbolicTile
from sorbetto.tile.utils import get_colors


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
        self._colormap = get_colors(len(self.entities))  # FIXME
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

    def flavorCall(self, importance):
        assert self.flavor is not None
        return self.flavor(
            importance=importance,
        )

    def getExplanation(self):
        return "Explanation of the entity tile not yet defined"
