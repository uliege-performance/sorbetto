# Copyright (c) 2025-2025, Sebastien Pierard et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import numpy as np

from sorbetto.core.entity import Entity
from sorbetto.core.importance import Importance
from sorbetto.flavor.abstract_numeric_flavor import AbstractNumericFlavor
from sorbetto.performance.finite_set_of_two_class_classification_performances import (
    FiniteSetOfTwoClassClassificationPerformances,
)
from sorbetto.ranking.ranking_score import RankingScore


class WorstFlavor(AbstractNumericFlavor):
    """
    TODO actual description

    Example of Worst Flavor: the Baseline Flavor.
    """

    def __init__(
        self,
        performances: FiniteSetOfTwoClassClassificationPerformances,
        entity_list: list[Entity],  # TODO: why is there this argument?
        name: str = "Unnamed Worst Flavor",
        colormap: Any = None,
    ):
        super().__init__(name=name, colormap=colormap)

        assert isinstance(performances, FiniteSetOfTwoClassClassificationPerformances)

        self._entity_list = entity_list
        self._nb_entities = len(entity_list)
        self._performances = performances

    @property  # TODO: why is there this property in this class?
    def entity_list(self) -> list[Entity]:
        return self._entity_list

    @property  # TODO: why is there this property in this class?
    def nb_entities(self) -> int:
        return self._nb_entities

    @property
    def performances(self) -> FiniteSetOfTwoClassClassificationPerformances:
        return self._performances

    def __call__(
        self,
        importance: Importance | np.ndarray,
    ) -> float | np.ndarray:
        values = RankingScore._compute(
            importance=importance, performance=self._performances
        )

        ans = np.min(values, axis=0, keepdims=False)
        if isinstance(ans, np.ndarray) and ans.size == 1:
            return ans.item()
        else:
            return ans

    def getDefaultColormap(self):
        return "gray"

    def getLowerBound(self) -> float:
        return 0.0

    def getUpperBound(self) -> float:
        return 1.0
