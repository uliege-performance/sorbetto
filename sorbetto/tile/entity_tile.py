# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from sorbetto.flavor.entity_flavor import EntityFlavor
from sorbetto.parameterization.abstract_parameterization import AbstractParameterization
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.tile.symbolic_tile import SymbolicTile


class EntityTile(SymbolicTile):
    def __init__(
        self,
        parameterization: AbstractParameterization,
        flavor: EntityFlavor,
        name: str = "Entity Tile",
        resolution: int = 1001,
        legend_mode: str = "default",
    ):
        assert isinstance(parameterization, AbstractParameterization)
        assert isinstance(flavor, EntityFlavor)
        assert isinstance(name, str)
        assert isinstance(resolution, int)
        assert resolution > 0

        super().__init__(
            parameterization=parameterization,
            flavor=flavor,
            name=name,
            resolution=resolution,
            legend_mode=legend_mode,
            base_constraint_on_importances=None,
        )
        self._rank = self.flavor.rank
        self._entities = self.flavor.entity_set
        self._colormap = self.flavor.colormap
        self._performance = self.flavor.performances

    @property
    def flavor(self) -> EntityFlavor:
        # We override the property's getter to ensure the right type of flavor.
        flavor = super().flavor
        assert isinstance(flavor, EntityFlavor)
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
    def rank(self) -> int:
        return self._rank

    @property
    def performance(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performance

    def getExplanation(self):
        return super().getExplanation()
